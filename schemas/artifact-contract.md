# Artifact contract（归档建议；非既有schema全量实现）
每件工件记录RUN_ID、worker/lane、输入版本、source_URL、capture_time、sha256、parse_status、evidence_class、verification_method/result、unknown、stop_condition。
判定层：DISCOVERED→CAPTURED→PARSED→PARTIAL_SOURCE_CHECK→EXECUTION_TEST→ACCEPTED，后一步不得由前一步自动推断。
artifact存在与Agent声称完成不构成验收；外部副作用需单独权限及幂等/核验。
