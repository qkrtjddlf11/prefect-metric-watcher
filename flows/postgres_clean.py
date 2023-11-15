# pylint: disable=C0114, C0115, C0116
# coding: utf-8

# TODO Prefect의 로그는 PostgreSQL에 저장되며, 주기적으로 삭제해주는 로직이 없어 직접 삭제를 수행해줘야 한다.
# 테이블의 디스크 용량 확보를 위해 타이트한 Vacuum 정책을 가져간다.
