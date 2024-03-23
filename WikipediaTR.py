from datasets import DatasetInfo, Features, Value, SplitGenerator, Split, load_dataset, GeneratorBasedBuilder, DownloadManager
import datasets

class MyDataset(datasets.GeneratorBasedBuilder):
    def _info(self):
        return datasets.DatasetInfo(
            description="Datasetim hakkında açıklama",
            features=datasets.Features({
                "id": datasets.Value("string"),
                "text": datasets.Value("string"),
            }),
            homepage="http://biligcrawlopenturkishdata.s3.amazonaws.com/WikipediaTR_1711140570.4848208/",
            citation="citation",
        )
    def _split_generators(self, dl_manager: DownloadManager):
        urls_to_download = {"train": "http://biligcrawlopenturkishdata.s3.amazonaws.com/WikipediaTR_1711140570.4848208/wikipedia_pages_1711140570.884399.warc.gz", "test": "http://biligcrawlopenturkishdata.s3.amazonaws.com/WikipediaTR_1711140570.4848208/wikipedia_pages_1711140570.884399.warc.gz"}
        downloaded_files = dl_manager.download_and_extract(urls_to_download)

        return [
            SplitGenerator(name=Split.TRAIN, gen_kwargs={"filepath": downloaded_files["train"]}),
            SplitGenerator(name=Split.TEST, gen_kwargs={"filepath": downloaded_files["test"]}),
        ]

    def _generate_examples(self, filepath):
        with open(filepath, encoding="utf-8") as f:
            for id_, line in enumerate(f):
                yield id_, {
                    "id": str(id_),
                    "text": line.strip(),
                }
