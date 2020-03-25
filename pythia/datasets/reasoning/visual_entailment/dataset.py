import copy
import json

import torch

from pythia.common.sample import Sample
from pythia.datasets.vqa.vqa2 import VQA2Dataset

LABEL_TO_INT_MAPPING = {"entailment": 0, "neutral": 1, "contradiction": 2}


class VisualEntailmentDataset(VQA2Dataset):
    def __init__(self, dataset_type, imdb_file_index, config, *args, **kwargs):
        super().__init__(dataset_type, imdb_file_index, config, *args, **kwargs)

        self._name = "visual_entailment"

    def load_item(self, idx):
        sample_info = self.imdb[idx]
        current_sample = Sample()

        processed_sentence = self.text_processor({"text": sample_info["sentence2"]})

        current_sample.text = processed_sentence["text"]
        if "input_ids" in processed_sentence:
            current_sample.update(processed_sentence)

        if self._use_features is True:
            # Remove sentence id from end
            identifier = sample_info["Flikr30kID"].split(".")[0]
            # Load img0 and img1 features
            sample_info["feature_path"] = "{}.npy".format(identifier)
            features = self.features_db[idx]
            current_sample.update(features)

        label = LABEL_TO_INT_MAPPING[sample_info["gold_label"]]
        current_sample.targets = torch.tensor(label, dtype=torch.long)

        return current_sample
