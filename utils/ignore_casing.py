
def ignore_casing(prefix):
    prefix = " ".join(prefix.split())
    return "".join(filter(lambda x: x.isalnum() or x.isspace(), prefix)).lower()
