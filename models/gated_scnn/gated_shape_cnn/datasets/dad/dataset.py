import os
import tensorflow as tf

from models.gated_scnn.gated_shape_cnn.datasets.dad.raw_dataset import DADRaw
from models.gated_scnn.gated_shape_cnn.training.dataset import Dataset


class DAD(Dataset):

    def __init__(
            self,
            batch_size,
            network_input_h,
            network_input_w,
            debug,
            data_dir,
            n_classes,
            seed):
        super(DAD, self).__init__(
            n_classes,
            batch_size,
            network_input_h,
            network_input_w,
            seed,
            debug)
        self.raw_data = DADRaw(data_dir, seed)
        
        # Build edge segs if needed (this may take a while)
        if not os.path.exists(os.path.join(data_dir, "edges")):
            print("Generating borderless masks, their corresponding edge masks, and re-generating masks with border. This may take a long time.")
            self.raw_data.build_edge_segs()

    def get_paths(self, train, is_test=False):
        """
        :param train:
        :return image_paths, label_paths, edge_paths:
            image_path[0] -> path to image 0
            label_paths[0] -> path to semantic seg of image 0
            edge_paths[0] -> path to edge seg of label 0
        """
        split = 'train' if train else 'valid'
        if is_test:
            split = 'test'
        paths = self.raw_data.dataset_paths(split)
        image_paths, label_paths, edge_paths = zip(*paths)
        return list(image_paths), list(label_paths), list(edge_paths)
