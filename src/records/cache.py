from dnslib.dns import DNSRecord, RR
from dnslib.server import DNSHandler
from .record import Record, RecordType
from .answer import Answer


class Cache(Record):

    @classmethod
    def insert(cls, host: str, _type: RecordType, rr):
        main_key = f"{host}:{_type}"
        ttl = 0
        answers = []
        for ans in rr:
            answer = ans.rdata.__str__()
            if ans.rtype == _type:
                answers.append(answer)
                ttl = min(ttl, ans.ttl)
                continue

            key = f"{cls.clean_host(ans.rname.__str__())}:{ans.rtype}"
            cls.r.lpush(key, answer)
            cls.r.expire(key, min(cls.r.ttl(key), ans.ttl))

        main_key = f"{host}:{_type}"
        cls.r.lpush(main_key, *answers)
        cls.r.expire(main_key, ttl)
