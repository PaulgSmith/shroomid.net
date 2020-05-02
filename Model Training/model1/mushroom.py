# coding=utf-8
# Copyright 2020 The TensorFlow Datasets Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Dataset class for Mashdataset dataset."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import fnmatch
import os

import tensorflow.compat.v2 as tf
import tensorflow_datasets.public_api as tfds

_CITATION ="""\
 @article
"""



_URL = "https://github.com/alweheiby/yy/blob/master/train.rar"
_NAMES=["A1000", "B10025", "C10052", "D10056", "F10057"]
_IMAGE_SHAPE =(None, None,3)

class Mushroom(tfds.core.GeneratorBasedBuilder):
  """Mushrooms small train dataset."""

  
  VERSION = tfds.core.Version('0.1.0')

  def _info(self):
    """Mshroom dataset Images Dataset Class."""
    
    return tfds.core.DatasetInfo(
        builder=self,
        description=_DESCRIPTION,
        features=tfds.features.FeaturesDict({
              "image": tfds.features.Image(shape=_IMAGE_SHAPE),
              "label": tfds.features.ClassLabel(names=_NAMES),
        }),
        supervised_keys=("image", "label"),
        homepage= "https://github.com/alweheiby/Mushroom1.git",
        citation=_CITATION,
    )

  def _split_generators(self, dl_manager):
    """Define Splits."""

    path = dl_manager.download_and_extract(_URL)

    return [
        tfds.core.SplitGenerator(
            name=tfds.Split.TRAIN,
            gen_kwargs={
                "data_dir_path": os.path.join(path, "train"),
            },
        ),
    ]

  def _generate_examples(self, data_dir_path):
    """Generate images and labels for splits."""
    folder_names = ["A1000", "B10025", "C10052", "D10056", "F10057"]

    for folder in folder_names:
      folder_path = os.path.join(data_dir_path, folder)
      for file_name in tf.io.gfile.listdir(folder_path):
        if fnmatch.fnmatch(file_name, "*.JPG"):
          image = os.path.join(folder_path, file_name)
          label = folder.lower()
          image_id = "%s_%s" % (folder, file_name)
          yield image_id, {"image": image, "label": label}
     