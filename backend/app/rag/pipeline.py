import re
import time
from typing import Protocol
from app.schemas import Chunk, QueryAnalysis, QueryEntities, RankedChunk

SERVICES={"stripe":"payments","paypal":"payments","payment":"payments","payments":"payments","charged":"payments","unpaid":"payments","declined":"payments","checkout":"commerce","cart":"commerce","order":"commerce","orders":"commerce","javascript":"frontend","react":"frontend","browser":"frontend","cors":"api","rest api":"api","api":"api","node.js":"backend","nodejs":"backend","authentication":"identity","oauth":"identity","login":"identity","docker":"containers","container":"containers","nginx":"web-server","postgresql":"database","postgres":"database","database":"database","kubernetes":"platform","k8s":"platform","pod":"platform","deployment":"platform","kafka":"event-streaming","consumer":"event-streaming","redis":"cache","cache":"cache"}

def _structured_answer(summary:str,causes:list[str],steps:list[str],checks:list[str],avoid:list[str]|None=None)->str:
    bullets="\n".join(f"- {item}" for item in causes)
    actions="\n".join(f"{index}. {item}" for index,item in enumerate(steps,1))
    verification="\n".join(f"- {item}" for item in checks)
    caution="" if not avoid else "\n\n## Avoid\n\n"+"\n".join(f"- {item}" for item in avoid)
    return f"## Short answer\n\n{summary}\n\n## Most likely causes\n\n{bullets}\n\n## Investigate in this order\n\n{actions}\n\n## How to confirm the fix\n\n{verification}{caution}"

def playbook_answer(question:str)->str|None:
    q=question.lower().replace("’","'")
    if "webhook" in q and any(term in q for term in ("500","5xx","failed","failure","error")):
        return _structured_answer(
            "An HTTP 500 means the provider reached your webhook endpoint, but your application failed while processing the event. Preserve the event, find the first server exception for that delivery, fix the handler, and then replay the same event safely.",
            ["The handler raised an exception while validating or transforming the event.","The event could not find its related order, payment, or customer record.","A database write, downstream API call, or timeout failed after the webhook was received.","The handler depends on event ordering or is not safe when the provider retries the same event."],
            ["Open the failed delivery in the provider dashboard and record its event ID, event type, timestamp, and response body.","Find the matching request in application logs and identify the first exception and failing operation.","Confirm the event belongs to the same account and environment as the related internal record.","Fix the handler and make it idempotent using the provider event ID before retrying.","Replay that exact event from the provider dashboard or a safe replay tool, then monitor the resulting order or payment state."],
            ["The replay returns a 2xx response and updates the intended record exactly once.","Replaying the event a second time is a harmless no-op.","New webhook deliveries complete without 5xx responses."],
            ["Do not generate a new charge to repair a failed webhook.","Do not return 2xx before durable processing unless the event has been safely queued."])
    if "charged" in q and ("unpaid" in q or "marked as unpaid" in q):
        return _structured_answer(
            "The payment provider probably completed the charge, but your application did not complete the separate step that updates the order. Treat this as a payment-to-order reconciliation failure, not as another card-payment attempt.",
            ["The provider webhook was not delivered, returned a non-2xx response, or failed signature verification.","The webhook was accepted but the order-update handler failed, timed out, or could not find the order.","The payment and order were created in different environments, or the provider ID was not stored against the order.","The event is still processing asynchronously, or duplicate/out-of-order events left the order in the wrong state."],
            ["Open the payment-provider dashboard and confirm the final payment status, event ID, amount, currency, and timestamp.","Find the matching webhook delivery. Check its event type, response status, retry history, and your application log at the same timestamp.","Trace the provider payment or capture ID to the internal order ID. Verify that the mapping exists and points to the correct environment.","Inspect the order-update transaction for validation errors, database failures, or an exception after the webhook was received.","After fixing the handler, replay the event or run a controlled reconciliation job. Make the operation idempotent so replaying it cannot create another charge or duplicate order update."],
            ["The provider shows the payment as completed and the internal order changes to paid exactly once.","Replaying the same event produces no duplicate charge, duplicate fulfilment, or second state transition.","New successful payments update their orders automatically and webhook deliveries return 2xx responses."],
            ["Do not ask the customer to pay again until the original provider transaction has been checked.","Do not manually mark the order paid without recording the provider transaction ID and an audit note."])
    if "payment button" in q and any(word in q for word in ("disappeared","missing","not showing","doesn't appear")):
        return _structured_answer(
            "Because the button disappeared immediately after a frontend deployment, start with the deployed JavaScript, runtime configuration, and third-party payment script, not the payment-processing backend.",
            ["A JavaScript exception stops rendering before the button component mounts.","The payment SDK script is blocked, missing, or rejected by Content Security Policy.","A production environment value such as the publishable key, client ID, currency, or feature flag is missing.","Conditional rendering now hides the button for the current cart, country, user, or payment state.","The browser or CDN is serving incompatible HTML and JavaScript versions."],
            ["Open Console and reload the page. Fix the first error, not the later cascade of errors.","In Network, confirm the application bundle and payment SDK load successfully with 2xx responses and are not blocked by CSP or an extension.","Compare the deployed public configuration and feature flags with the previous working release. Never expose secret keys in the browser.","Inspect the button component's render conditions using the exact failing cart and user state.","Test a private window, clear the service-worker/CDN cache if applicable, and compare against a rollback or the previous build."],
            ["The button appears with no Console errors in a clean browser session.","The payment SDK initializes once and the button works in both test and intended production configuration.","A canary deployment succeeds before the release is promoted to all users."],
            ["Do not put server-side payment secrets into frontend environment variables."])
    if "duplicate" in q and any(word in q for word in ("payment","charge","order")):
        return _structured_answer(
            "The retry path is probably creating a new payment instead of safely resuming the original operation. The fix is end-to-end idempotency, not disabling retries.",
            ["The client generates a new idempotency key after refresh or timeout.","The backend does not persist the key and result atomically.","A webhook and synchronous callback both perform the same fulfilment action.","The user can submit the payment action more than once while the first request is pending."],
            ["Trace both charges and compare request IDs, idempotency keys, order IDs, and timestamps.","Create one stable idempotency key per order/payment attempt and reuse it across uncertain retries.","Store the key, provider transaction ID, and result in the same durable transaction as the order state change.","Make webhook processing idempotent using the provider event ID.","Disable repeated UI submission for usability, but keep backend idempotency as the actual protection."],
            ["Repeating the same request returns the original result and creates only one provider transaction.","Replaying a webhook does not repeat fulfilment or change the order twice."],None)
    if "declined" in q and any(word in q for word in ("one customer","other customers","others can")):
        return _structured_answer(
            "Because other customers can pay, the integration is probably healthy. Treat this as a payment-method or customer-specific decline and use the provider's safe decline code to guide the next action.",
            ["The issuer declined the card for funds, risk, authentication, or card-status reasons.","The payment requires customer authentication such as 3-D Secure.","The billing details, currency, country, or merchant restrictions do not match.","The provider's fraud controls blocked this specific attempt."],
            ["Locate the failed attempt in the provider dashboard using its request or payment ID.","Read the provider's decline code and recommended customer-facing message; do not rely only on your application's generic error.","Confirm whether additional authentication is required and whether the customer completed it.","Ask the customer to retry once or use another payment method when the provider recommends it.","Escalate to the provider with the safe transaction identifier if repeated valid methods fail."],
            ["A supported payment method completes successfully and the provider records a successful final status.","The user sees a clear, non-sensitive message rather than a raw provider response."],
            ["Do not request or log the full card number, CVC, password, or authentication code."])
    if "test mode" in q and ("live" in q or "production" in q):
        return _structured_answer(
            "A test-only success usually means the live environment is using different credentials, account capabilities, webhook configuration, domains, or payment-method settings.",
            ["Test and live client/server credentials are mixed.","The live account or payment method is not activated for the currency or country.","Live webhook endpoints or signing secrets were not configured separately.","Production domains, redirect URLs, or Content Security Policy differ from test."],
            ["Verify that every frontend key, backend key, account ID, and endpoint belongs to the same live environment.","Check live-account activation, enabled payment methods, currencies, and required business verification.","Compare live and test webhook URLs, subscribed events, signing secrets, and recent delivery results.","Compare allowed domains, redirect URLs, CSP, and proxy configuration.","Run one controlled live transaction and correlate the browser request, server log, provider request ID, and webhook."],
            ["The controlled live transaction reaches a final successful provider status and updates the internal order.","Live webhook deliveries return 2xx and no test identifiers appear in production logs."],
            ["Never copy test secrets into production or expose secret keys in browser code."])
    if "cors" in q and any(word in q for word in ("stripe","checkout","payment")):
        return _structured_answer(
            "A browser CORS error during checkout usually means the frontend is calling an endpoint that is not intended for direct cross-origin browser access, or your own backend is not handling the browser's preflight request correctly.",
            ["The frontend calls a provider's secret API directly instead of your backend or the provider's browser SDK.","Your API does not answer OPTIONS with the required origin, method, and header permissions.","A redirect or proxy sends the request to a different origin that does not allow the application domain.","Custom headers trigger a preflight that the server or gateway rejects."],
            ["Identify the exact failed request in Network and read the Console's CORS reason.","If it targets a provider secret API, move that call to the backend and use the supported browser SDK on the client.","If it targets your API, verify the OPTIONS response and Access-Control-Allow-Origin, Methods, Headers, and Credentials settings.","Check redirects, reverse proxies, and environment URLs for an unexpected origin change.","Retest from the real application origin—not from a local file—and verify both preflight and actual request."],
            ["The OPTIONS request succeeds and the actual request follows.","No secret provider credential appears in browser source, requests, or logs."],
            ["Do not use no-cors as a fix; it hides the response from JavaScript and does not grant access."])
    return None

def needs_clarification(query:str)->bool:
    lower=query.lower().replace("’", "'")
    vague=any(re.search(pattern,lower) for pattern in (r"doesn'?t work",r"doesnt work",r"not working",r"is broken",r"something went wrong",r"having (?:an )?issue",r"there is (?:an )?issue",r"i have (?:a )?problem"))
    concrete=bool(re.search(r"\b(?:[45]\d\d|[a-z]{2,10}-\d{2,6}|v?\d+\.\d+|timeout|declined|blank|redirect|cors|console|network|stripe|paypal)\b",lower))
    return vague and not concrete and len(re.findall(r"\w+",lower))<=18

def clarification_answer(question:str)->str:
    lower=question.lower()
    if any(word in lower for word in ("website","client side","client-side","frontend","front end","browser","react","javascript","page","ui","blank screen","crash")):
        return """## Short answer

A client-side website crash is usually caused by a JavaScript runtime exception, a failed application or asset request, an incompatible browser condition, unexpected page data, or excessive memory use. The first Console error and its stack trace are needed to identify which one is happening.

## Check these first

1. Reproduce the crash and record the exact page, button, or action that triggers it.
2. Open the browser developer tools, select Console, reproduce the crash, and copy the first red error and stack trace. Later errors may only be consequences of the first one.
3. Check the Network panel for failed JavaScript chunks, API requests, images, or configuration files. Record the failed URL and HTTP status.
4. Test the same action in a private window and another supported browser. This separates application failures from stale cache, extensions, or browser-specific behaviour.
5. Compare the time the crashes began with the latest frontend deployment, dependency update, feature flag, CDN change, or API response change.
6. If the entire browser tab closes or freezes, inspect memory usage and test with a smaller dataset or disabled browser extensions.

## Send these details

- The first Console error and stack trace.
- The affected page URL, browser and version, environment, and frontend release or commit.
- Exact reproduction steps and whether every user is affected.
- Any failed Network request, including its URL, status, and response summary without personal data or tokens.

## What happens next

ResolveAI can use those details to distinguish a code exception, deployment or caching problem, failed dependency, bad API response, or browser resource issue and retrieve a matching solved case."""
    if any(word in lower for word in ("payment","checkout","card","stripe","paypal")):
        return """## Short answer

There is not enough detail yet to identify the payment failure safely. It may originate in the checkout page, application API, payment provider, authentication step, or network connection, so changing configuration now would be guesswork.

## Check these first

1. Confirm whether the problem affects every user or only one account, browser, device, or payment method.
2. Record exactly what appears: a blank form, endless loading, redirect loop, decline, or visible error message.
3. In browser developer tools, note the first Console error and the failing Network request's URL and HTTP status.
4. Check whether test and live credentials have been mixed and whether the provider dashboard contains a matching request or event.
5. Record recent deployments, API-key changes, domain changes, webhook changes, and the provider's current service status.

## Send these details

- The provider, environment, exact error, timestamp, request ID, and affected payment method.
- Whether all users are affected and whether the same payment succeeds in the test environment.
- Do not include passwords, API secrets, card numbers, tokens, or personal data.

## What happens next

With those details, ResolveAI can retrieve a matching payment case and provide source-backed recovery steps."""
    if any(word in lower for word in ("login","authentication","oauth","sign in","signin","token")):
        return """## Short answer

The report points to an identity or session problem, but the exact failure stage is missing. First determine whether it fails before credentials are submitted, during the identity-provider redirect, or after the application receives the callback.

## Check these first

1. Record the exact message and the last URL visible before the failure or redirect loop.
2. Check the browser Console and Network panels for failed authorization, token, callback, or session requests.
3. Confirm the redirect URI, application client ID, environment, cookie domain, and system clock without exposing secrets.
4. Test a private window and a second user to separate stale cookies from an application-wide failure.
5. Compare the start time with identity-provider, certificate, domain, proxy, or application deployments.

## Send these details

- Identity provider, environment, HTTP status, safe error code, request ID, redirect path, and affected-user scope.
- Never include passwords, authorization codes, access tokens, client secrets, or cookies.

## What happens next

ResolveAI can then retrieve a relevant OAuth, redirect, cookie, or session case instead of guessing."""
    if any(word in lower for word in ("docker","container","kubernetes","pod")):
        return """## Short answer

The container symptom needs a failing command, log message, or connection before a specific cause can be identified. Common categories include startup configuration, missing environment values, networking, permissions, storage, and resource limits.

## Check these first

1. Capture the container or pod status, exit code, restart count, and first relevant error in its logs.
2. Confirm the image version, command, environment names, mounted files, ports, and target hostname without exposing secret values.
3. Test DNS resolution and connectivity from inside the same container or pod.
4. Check recent image, deployment, network-policy, volume, or resource-limit changes.
5. Compare one failing instance with a healthy instance if available.

## Send these details

- Platform, image version, status, exit code, safe log excerpt, destination host and port, and recent change.

## What happens next

ResolveAI can then match the failure to a real container or Kubernetes case and provide focused recovery steps."""
    if any(word in lower for word in ("database","postgres","postgresql","redis","sql","query")):
        return """## Short answer

The database symptom needs the exact server or client error before it is safe to recommend a change. Connection, authentication, permissions, locking, capacity, and query problems require different remedies.

## Check these first

1. Capture the complete error code and message, database product and version, and client or application name.
2. Determine whether the problem affects every query, one operation, or one user.
3. Check connection availability, authentication method, permissions, active sessions, storage, and recent configuration changes.
4. Record the timestamp and correlate it with database and application logs using a request ID when available.
5. Test the same operation in a safe non-production environment before changing production settings.

## Send these details

- Exact error, database version, operation, affected scope, environment, timestamp, and recent change. Remove credentials and customer data.

## What happens next

ResolveAI can then retrieve the relevant connection, permission, capacity, or query case."""
    return """## Short answer

The symptom is too broad to connect safely to one cause. The exact error, affected component, scope, and most recent change are needed before applying a fix.

## Check these first

1. Record the precise action that fails and the exact visible error.
2. Confirm whether every user and environment is affected or only one account, device, or request.
3. Capture the earliest relevant application log, browser Console error, or failed request status.
4. Record when it began and what deployment, configuration, dependency, certificate, or infrastructure change happened immediately beforehand.
5. Compare the failing behaviour with one known-good environment or instance.

## Send these details

- Component, environment, version, timestamp, reproduction steps, exact error, request ID, affected scope, and recent change.
- Remove passwords, tokens, personal data, and secrets.

## What happens next

ResolveAI can use those details to retrieve a matching solved case rather than offering an unrelated generic fix."""

class QueryAnalyzer:
    def analyze(self,query:str)->QueryAnalysis:
        lower=query.lower(); errors=sorted(set(re.findall(r"\b[A-Z]{2,8}-\d{3}\b",query.upper())))
        versions=sorted(set(re.findall(r"(?<!\d)(?:v)?(\d+\.\d+(?:\.\d+)?)(?!\d)",query)))
        services=sorted({canonical for token,canonical in SERVICES.items() if re.search(rf"(?<!\w){re.escape(token)}(?!\w)",lower)})
        if any(token in lower for token in ("stripe","paypal","payment","charged","unpaid","declined")): services=["payments"]
        tech=[]
        for name in ["PostgreSQL 16","PostgreSQL","Kubernetes","Kafka","Redis","OpenSearch"]:
            if name.lower() in lower: tech.append(name)
        env=[e for e in ["production","staging","development"] if e in lower]
        intent="incident_resolution" if any(x in lower for x in ["why","caused","incident","resolve","fixed"]) else "knowledge_lookup"
        anchors=" ".join(errors+versions+services+tech)
        rewritten=f"{query.strip()} Historical incidents, current troubleshooting guidance, root cause, resolution and verification. Preserve identifiers: {anchors}."
        filters={}
        if len(services)==1: filters["service"]=services[0]
        sub=[query, f"{anchors} root cause incident".strip(), f"{anchors} remediation runbook".strip()]
        return QueryAnalysis(original_query=query,intent=intent,rewritten_query=rewritten,entities=QueryEntities(services=services,versions=versions,error_codes=errors,technologies=tech,environment=env),filters=filters,subqueries=list(dict.fromkeys(sub)))

class ContextBuilder:
    AUTHORITY={"runbook":5,"troubleshooting":5,"public_reference":5,"product_doc":4,"release_note":4,"community_support":3,"incident":3,"support_ticket":2}
    def select(self,candidates:list[RankedChunk],limit:int=6)->list[RankedChunk]:
        seen_text,per_doc,result=set(),{},[]
        ordered=sorted(candidates,key=lambda c:((c.reranker_score or 0)+.01*self.AUTHORITY.get(c.chunk.document_type,1),c.chunk.updated_at),reverse=True)
        for item in ordered:
            signature=" ".join(item.chunk.text.lower().split()[:35])
            if signature in seen_text or per_doc.get(item.chunk.document_id,0)>=3: continue
            seen_text.add(signature); per_doc[item.chunk.document_id]=per_doc.get(item.chunk.document_id,0)+1; result.append(item)
            if len(result)>=limit: break
        return result

class LLM(Protocol):
    def generate(self,question:str,context:list[RankedChunk],history:list[dict]|None=None)->str: ...

class MockLLM:
    def generate(self,question:str,context:list[RankedChunk],history:list[dict]|None=None)->str:
        playbook=playbook_answer(question)
        if playbook: return playbook
        if not context: return clarification_answer(question)
        meaningful={word for word in re.findall(r"[a-z0-9-]+",question.lower()) if len(word)>2 and word not in {"what","when","where","which","should","does","with","from","this","that","after","before","could","would"}}
        accepted_rows=[]
        for item in context:
            if item.chunk.document_type!="community_support" or item.chunk.section_title.lower()!="accepted answer": continue
            title_words=set(re.findall(r"[a-z0-9-]+",item.chunk.title.lower()))
            accepted_rows.append((len(meaningful&title_words)/max(1,len(meaningful)),item))
        accepted=max(accepted_rows,default=(0,None),key=lambda row:row[0])[1] if accepted_rows and max(row[0] for row in accepted_rows)>=.45 else None
        if accepted:
            doc_id=accepted.chunk.document_id
            raw=re.sub(r"```.*?```","",accepted.chunk.text,flags=re.S)
            raw=re.sub(r"(PASSWORD\s+)'[^']+'",r"\1 '<new-strong-password>'",raw,flags=re.I)
            lines=[]
            for value in raw.splitlines():
                value=value.replace("`","")
                value=re.sub(r"^[#*\-\s]+|[*\s]+$","",value).strip()
                value=re.sub(r"\s+"," ",value)
                if not value or value.lower()=="accepted answer" or value=="[]" or len(value)<18: continue
                if value not in lines: lines.append(value)
            direct=" ".join(lines[:2]) if lines else "The accepted answer contains a documented solution for this problem."
            starters=("you can","after","if ","find ","edit ","restart ","connect ","run ","remove ","change ","check ","create ","use ","set ","open ","add ","choose ","make ","ensure ","try ")
            actions=[line for line in lines[2:] if line.lower().startswith(starters) and not line.endswith(":") and len(line)<=320][:5]
            if not actions: actions=lines[2:7]
            checks=[line for line in lines if any(word in line.lower() for word in ("verify","confirm","connect","check","test","expected","change it back","remove the line")) and line not in actions][:3]
            if not checks: checks=actions[-2:]
            def listed(rows:list[str],numbered:bool)->str:
                return "\n".join(f"{index}. {line} [{doc_id}]" if numbered else f"- {line} [{doc_id}]" for index,line in enumerate(rows,1))
            return f"## Short answer\n\n{direct} [{doc_id}]\n\n## What to do now\n\n{listed(actions,True)}\n\n## How to confirm it is fixed\n\n{listed(checks,False)}\n\n## Important safety note\n\n- Apply the accepted answer to a non-production environment first when possible. If you temporarily relax authentication or access controls, restore the secure setting immediately after completing the documented change. [{doc_id}]\n\n## If the problem continues\n\n- Recheck the exact error message, product version, and configuration path, then compare them with the original question.\n- Escalate with the error, timestamps, configuration changes, and the checks you already completed.\n\n## Sources\n\n- **{accepted.chunk.title}** - accepted Stack Overflow answer [{doc_id}]"
        if not accepted: return clarification_answer(question)
        query_terms={t for t in re.findall(r"[a-z0-9-]+",question.lower()) if len(t)>2 and t not in {"what","when","where","which","after","with","does","from","have","this","that"}}
        candidates=[]
        for item in context:
            clean=re.sub(r"[#*`]", "",item.chunk.text).replace("\n"," ")
            for sentence in re.split(r"(?<=[.!?])\s+",clean):
                sentence=re.sub(r"\s+"," ",sentence).strip(" -")
                if not 45<=len(sentence)<=420: continue
                terms=set(re.findall(r"[a-z0-9-]+",sentence.lower()))
                score=len(query_terms&terms)/max(1,len(query_terms))
                candidates.append((score,sentence,item))
        candidates.sort(key=lambda row:row[0],reverse=True)
        def select(keywords:set[str],limit:int,exclude:set[str]|None=None):
            selected=[]; seen=set(); exclude=set() if exclude is None else exclude
            for score,sentence,item in candidates:
                lower=sentence.lower()
                if sentence in exclude or any(noise in lower for noise in ["this appendix preserves","following internal notes","phase objective"]): continue
                if keywords and not any(word in lower for word in keywords): continue
                signature=" ".join(lower.split()[:10])
                if signature in seen: continue
                seen.add(signature); selected.append((sentence,item)); exclude.add(sentence)
                if len(selected)>=limit: break
            return selected
        used=set()
        causes=select({"root cause","caused","introduced","exhaust","because","confirmed"},1,used)
        if not causes: causes=select(set(),1,used)
        actions=select({"resolution","resolved","fix","deployed","reduced","set ","rollback","restore","disable","change"},4,used)
        checks=select({"verify","check","monitor","confirm","canary","inspect","compare","validate"},3,used)
        if not actions: actions=select(set(),3,used)
        if not checks: checks=select(set(),3,used)
        service_name=next((item.chunk.service.replace("-"," ").title() for item in context if item.chunk.service not in {"platform",""}),"The affected service")
        def polish(sentence:str,kind:str)->str:
            sentence=re.sub(r"^(Investigation and root cause|Summary and impact|Resolution and recovery)\s+","",sentence,flags=re.I)
            if sentence.lower().startswith("the confirmed root cause was "):
                detail=sentence[len("The confirmed root cause was "):]
                detail=re.sub(r"^(\d+(?:\.\d+)+)\s+",r"Version \1 ",detail)
                return f"The issue was caused by a version-specific change in {service_name}: {detail}"
            if sentence.lower().startswith("the documented remediation is:"):
                return "Apply the documented fix: "+sentence.split(":",1)[1].strip()
            if sentence.lower().startswith("for ") and "catalog definition is:" in sentence.lower():
                before,after=sentence.split(":",1)
                code=before.split(",",1)[0].replace("For ","")
                return f"{code} means {after.strip()[0].lower()+after.strip()[1:]}"
            if sentence.lower().startswith("rollback remains available"):
                return "Keep the rollback option available until all verification checks pass."
            return sentence
        def cited(rows,numbered=False,kind="detail"):
            lines=[]
            for index,(sentence,item) in enumerate(rows,1):
                prefix=f"{index}." if numbered else "-"
                lines.append(f"{prefix} {polish(sentence,kind)} [{item.chunk.document_id}]")
            return "\n".join(lines)
        direct=polish(causes[0][0],"cause") if causes else "The available records point to a service or dependency configuration problem."
        direct_source=causes[0][1].chunk.document_id if causes else context[0].chunk.document_id
        evidence=[]
        for item in context:
            line=f"- **{item.chunk.title}** — {item.chunk.section_title} [{item.chunk.document_id}]"
            if line not in evidence: evidence.append(line)
        return f"## Short answer\n\n{direct} [{direct_source}]\n\n## What to do now\n\n{cited(actions,True,'action')}\n\n## How to confirm it is fixed\n\n{cited(checks,False,'check')}\n\n## If the problem continues\n\n- Escalate to the {service_name} owner if these checks do not confirm the cause, multiple services are affected, or recovery would require an undocumented production change.\n- Include request IDs, timestamps, affected versions, and before-and-after metrics so the next team can continue without repeating your work.\n\n## Sources\n\n"+"\n".join(evidence)

class GroqLLM:
    def __init__(self,api_key:str,model:str): self.api_key,self.model=api_key,model
    def generate(self,question:str,context:list[RankedChunk],history:list[dict]|None=None)->str:
        if not self.api_key or not self.model: return MockLLM().generate(question,context,history)
        import json,urllib.request
        evidence="\n\n".join(f"[{c.chunk.document_id}] {c.chunk.title} / {c.chunk.section_title}\n{c.chunk.text}" for c in context)
        prompt=_grounded_prompt(question,evidence)
        messages=[{"role":"system","content":SYSTEM_PROMPT},*(history or []),{"role":"user","content":prompt}]
        request=urllib.request.Request("https://api.groq.com/openai/v1/chat/completions",data=json.dumps({"model":self.model,"messages":messages,"temperature":0}).encode(),headers={"Authorization":f"Bearer {self.api_key}","Content-Type":"application/json"})
        with urllib.request.urlopen(request,timeout=30) as response: return json.load(response)["choices"][0]["message"]["content"]


SYSTEM_PROMPT="""You are ResolveAI, a careful technical support assistant for administrators. Write concise, clear Markdown. Never copy an irrelevant source. Separate confirmed facts from likely causes. Use exactly these useful sections when applicable: Short answer, Most likely causes, Investigate in this order, How to confirm the fix, and Avoid. Cite evidence-backed claims with [document_id]. If the evidence does not establish a root cause, say so plainly and give safe diagnostic steps instead of inventing one. Use the earlier conversation only to understand follow-up questions."""


def _grounded_prompt(question:str,evidence:str)->str:
    evidence=evidence or "No sufficiently relevant source was retrieved. Provide only general, safe diagnostic guidance and do not invent citations."
    return f"CURRENT QUESTION:\n{question}\n\nRETRIEVED EVIDENCE:\n{evidence}\n\nAnswer the current question directly. Do not repeat the conversation or expose retrieval details."


class OllamaLLM:
    def __init__(self,url:str,model:str): self.url,self.model=url.rstrip("/"),model
    def generate(self,question:str,context:list[RankedChunk],history:list[dict]|None=None)->str:
        import json,urllib.request
        evidence="\n\n".join(f"[{c.chunk.document_id}] {c.chunk.title} / {c.chunk.section_title}\n{c.chunk.text}" for c in context)
        messages=[{"role":"system","content":SYSTEM_PROMPT},*(history or []),{"role":"user","content":_grounded_prompt(question,evidence)}]
        request=urllib.request.Request(f"{self.url}/api/chat",data=json.dumps({"model":self.model,"messages":messages,"stream":False,"options":{"temperature":0}}).encode(),headers={"Content-Type":"application/json"})
        with urllib.request.urlopen(request,timeout=90) as response: return json.load(response)["message"]["content"]


def find_ollama_model(url:str,preferred:str="")->str:
    import json,urllib.request
    try:
        with urllib.request.urlopen(f"{url.rstrip('/')}/api/tags",timeout=1.2) as response:
            models=[item.get("name","") for item in json.load(response).get("models",[])]
        if preferred and preferred in models: return preferred
        return models[0] if models else ""
    except Exception:
        return ""

def validate_citations(answer:str,context:list[RankedChunk])->tuple[str,float,float]:
    available={c.chunk.document_id for c in context}; cited=re.findall(r"\[([A-Z]+(?:-[A-Z0-9.]+)+)\]",answer)
    valid=[c for c in cited if c in available]; invalid=set(cited)-available
    for citation in invalid: answer=answer.replace(f"[{citation}]","")
    validity=len(valid)/len(cited) if cited else 0.0; coverage=len(set(valid))/len(available) if available else 0.0
    return answer,validity,coverage

def evidence_label(context:list[RankedChunk],validity:float)->tuple[str,str]:
    docs=len({c.chunk.document_id for c in context}); top=context[0].reranker_score if context else 0
    if docs>=3 and validity>=.8 and (top or 0)>=.35: return "High evidence support","Multiple independent, well-ranked sources are cited."
    if docs>=1 and validity>=.5: return "Moderate evidence support","Relevant evidence was found, but source diversity or citation coverage is limited."
    return "Insufficient evidence","The retrieved evidence is too weak or insufficiently cited for a reliable answer."
