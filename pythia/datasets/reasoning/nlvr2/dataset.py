import json
import torch
import copy

from pythia.datasets.vqa.vqa2 import VQA2Dataset
from pythia.common.sample import Sample


class NLVR2Dataset(VQA2Dataset):
    def __init__(self, dataset_type, imdb_file_index, config, *args, **kwargs):
        super().__init__(dataset_type, imdb_file_index, config, *args, **kwargs)

        self._name = "nlvr2"

    def load_item(self, idx):
        sample_info = self.imdb[idx]
        current_sample = Sample()

        processed_sentence = self.text_processor({"text": sample_info["sentence"]})

        current_sample.text = processed_sentence["text"]
        if "input_ids" in processed_sentence:
            current_sample.update(processed_sentence)


        if self._use_features is True:
            # Remove sentence id from end
            identifier = "-".join(sample_info["identifier"].split("-")[:-1])
            # Load img0 and img1 features
            sample_info["feature_path"] = "{}-img0.npy".format(identifier)
            features = self.features_db[idx]
            current_sample.img0 = Sample()
            current_sample.img0.update(features)

            sample_info["feature_path"] = "{}-img1.npy".format(identifier)
            features = self.features_db[idx]
            current_sample.img1 = Sample()
            current_sample.img1.update(features)

        is_correct = 1 if sample_info["label"] == "True" else 0
        current_sample.targets = torch.tensor(is_correct, dtype=torch.long)

        return current_sample
