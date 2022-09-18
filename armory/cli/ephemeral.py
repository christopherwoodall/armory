
try:
    from armory.cli import CLI
except Exception as e:
    print(f"ERROR: {e}", file=sys.stderr)
    sys.exit(5)


class EphemeralCLI(CLI):
    def process(self, args):
        # super(EphemeralCLI, self).setup()
        ...


def main():
    EphemeralCLI().process(None)
