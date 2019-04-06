import settings
import json
import os
from module.GxdsHandler import GxdsHandler
from module.BdHandler import BdHandler
from module.OutHandler import OutHandler
from module.ColorLogDecorator import ColorLogDecorator


def main():
    dataset1 = GxdsHandler(settings.ROOT_DIR_GXDS, False)
    dataset2 = BdHandler(settings.ROOT_DIR_BD, False)
    dataset_final = OutHandler(settings.ROOT_OUTPUT, settings.THRESHOLD_COS, settings.THRESHOLD_PRE, False)

    for item1 in dataset1.poems():
        dataset_final.insert(item1)

    for item2 in dataset2.poems():
        dataset_final.insert(item2)

    if settings.OUTPUT_SUMMARY:
        with open(os.path.join(settings.ROOT_OUTPUT, "国学大师统计.json"), "w+", encoding="utf-8") as f:
            json.dump({
                "summary": dataset1.summary,
                "dynasty": dataset1.dynasties_summary
            }, f, ensure_ascii=False, indent=4)
        with open(os.path.join(settings.ROOT_OUTPUT, "国学大师诗人统计.json"), "w+", encoding="utf-8") as f:
            json.dump({
                "poets": dataset1.dynasties_poets
            }, f, ensure_ascii=False, indent=4)

        with open(os.path.join(settings.ROOT_OUTPUT, "八斗文学统计.json"), "w+", encoding="utf-8") as f:
            json.dump({
                "summary": dataset2.summary,
                "dynasty": dataset2.dynasties_summary
            }, f, ensure_ascii=False, indent=4)
        with open(os.path.join(settings.ROOT_OUTPUT, "八斗文学诗人统计.json"), "w+", encoding="utf-8") as f:
            json.dump({
                "poets": dataset2.dynasties_poets
            }, f, ensure_ascii=False, indent=4)

        with open(os.path.join(settings.ROOT_OUTPUT, "合并数据集统计.json"), "w+", encoding="utf-8") as f:
            json.dump({
                "summary": dataset_final.summary,
                "dynasty": dataset_final.dynasties_summary
            }, f, ensure_ascii=False, indent=4)
        with open(os.path.join(settings.ROOT_OUTPUT, "合并数据集诗人统计.json"), "w+", encoding="utf-8") as f:
            json.dump({
                "poets": dataset_final.dynasties_poets
            }, f, ensure_ascii=False, indent=4)

    print(ColorLogDecorator.green(" DONE ", "bg-strong"))


if __name__ == "__main__":
    main()
