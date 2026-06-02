import json

def main():
    group = json.load(open('runs/v3_B_group_openai_20260602T164705391436.json', encoding='utf8'))
    for r in group['results']:
        if r['result']['failures']:
            print(f"Fail in Group v3: {r['case']['id']} - {r['result']['failures']}")
            print(f"Expected: {r['case']['expect']}")
            print(f"Actual: {r['result'].get('actual_tool_calls')}")
            print()

    base0 = json.load(open('runs/v0_B_base_openai_20260602T144953773033.json', encoding='utf8'))
    count = 0
    for r in base0['results']:
        if r['result']['failures'] and count < 3:
            print(f"Fail in Base v0: {r['case']['id']} - {r['result']['failures']}")
            print(f"Expected: {r['case']['expect']}")
            print(f"Actual: {r['result'].get('actual_tool_calls')}")
            print()
            count += 1

if __name__ == '__main__':
    main()
