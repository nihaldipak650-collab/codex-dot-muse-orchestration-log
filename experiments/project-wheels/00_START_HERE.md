# PROJECT-WHEELS-100-V2

RUN_ID_PREFIX: PWV2-20261004
STATUS: ACTIVE
TARGET_TOTAL: 100

## Fixed directions
1. 文献助手
2. 动画
3. 游戏
4. 网站
5. 科研SOP

## Per-direction quota
- GitHub: 10
- X: 5
- YouTube: 5
- Total per direction: 20
- Grand total: 100

## Exclusions
- PROJECT-WHEELS-100 / PW-001..PW-100 are preserved as V1 and do not count toward V2.
- The separate AI×生物 20-candidate set remains separate and does not count toward V2.
- No duplicate entity / repo / creator / video / thread may count twice unless the reusable asset is materially different.

## Candidate test
Each item must map to:
- current project problem
- reusable wheel / technique / reference
- what can be copied or adapted
- boundary / why it is not a drop-in solution
- primary link
- source type
- verification status

## Loop idempotency
Each outbound Muse task carries a unique RUN_ID.
Before send, after send failure, and before retry:
1. search current Muse thread for RUN_ID;
2. if RUN_ID already appears as a user message, do NOT resend;
3. wait/read for assistant response;
4. retry only when RUN_ID is absent after refresh/recheck.
