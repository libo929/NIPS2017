# Copyright (c) 2017 Jes Frellsen and Wouter Boomsma. All Rights Reserved.
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
# =============================================================================

import tensorflow as tf

from CubedSphereBaseModel import CubedSphereBaseModel


class CubedSphereBandedDisjointModel(CubedSphereBaseModel):
    """Cubed Sphere model with banded disjoint r layers"""

    def _init_model(self,
                    patches_size_high_res,
                    r_size_high_res,
                    xi_size_high_res,
                    eta_size_high_res,
                    channels_high_res,
                    output_size):

        self.output_size = output_size

        self.x_high_res = tf.placeholder(tf.float32, [None, patches_size_high_res, r_size_high_res, xi_size_high_res, eta_size_high_res, channels_high_res])

        self.y = tf.placeholder(tf.float32, [None, output_size])

        self.dropout_keep_prob = tf.placeholder(tf.float32)

        ### LAYER 0 ###
        self.layers = [{'input': self.x_high_res}]
        self.print_layer(self.layers, -1, 'input')

        ### LAYER 1 ###
        self.layers.append({})
        self.layers[-1].update(self.create_cubed_sphere_conv_banded_disjoint_layer(len(self.layers)-1,
                                                                                   self.layers[-2]['input'],
                                                                                   ksize_r=3,
                                                                                   ksize_xi=5,
                                                                                   ksize_eta=5,
                                                                                   channels_out=16,
                                                                                   stride_r=1,
                                                                                   stride_xi=2,
                                                                                   stride_eta=2,
                                                                                   use_r_padding=False))
        self.layers[-1]['activation'] = tf.nn.relu(self.layers[-1]['conv'])
        self.layers[-1].update(self.create_cubed_sphere_avgpool_layer(len(self.layers)-1,
                                                                      self.layers[-1]['activation'],
                                                                      ksize_r=1,
                                                                      ksize_xi=3,
                                                                      ksize_eta=3,
                                                                      stride_r=1,
                                                                      stride_xi=2,
                                                                      stride_eta=2,
                                                                      use_r_padding=False))
        self.print_layer(self.layers, -1, 'activation')
        self.print_layer(self.layers, -1, 'pool')
        
        ### LAYER 2 ###
        self.layers.append({})
        self.layers[-1].update(self.create_cubed_sphere_conv_banded_disjoint_layer(len(self.layers)-1,
                                                                                   self.layers[-2]['pool'],
                                                                                   ksize_r=3,
                                                                                   ksize_xi=3,
                                                                                   ksize_eta=3,
                                                                                   channels_out=32,
                                                                                   stride_r=1,
                                                                                   stride_xi=1,
                                                                                   stride_eta=1,
                                                                                   use_r_padding=False))
        self.layers[-1]['activation'] = tf.nn.relu(self.layers[-1]['conv'])
        self.layers[-1].update(self.create_cubed_sphere_avgpool_layer(len(self.layers)-1,
                                                                      self.layers[-1]['activation'],
                                                                      ksize_r=3,
                                                                      ksize_xi=3,
                                                                      ksize_eta=3,
                                                                      stride_r=2,
                                                                      stride_xi=2,
                                                                      stride_eta=2,
                                                                      use_r_padding=False))
        self.print_layer(self.layers, -1, 'activation')
        self.print_layer(self.layers, -1, 'pool')


        ### LAYER 3 ###
        self.layers.append({})
        self.layers[-1].update(self.create_cubed_sphere_conv_banded_disjoint_layer(len(self.layers)-1,
                                                                                   self.layers[-2]['pool'],
                                                                                   ksize_r=3,
                                                                                   ksize_xi=3,
                                                                                   ksize_eta=3,
                                                                                   channels_out=64,
                                                                                   stride_r=1,
                                                                                   stride_xi=1,
                                                                                   stride_eta=1,
                                                                                   use_r_padding=False))
        self.layers[-1]['activation'] = tf.nn.relu(self.layers[-1]['conv'])
        self.layers[-1].update(self.create_cubed_sphere_avgpool_layer(len(self.layers)-1,
                                                                      self.layers[-1]['activation'],
                                                                      ksize_r=1,
                                                                      ksize_xi=3,
                                                                      ksize_eta=3,
                                                                      stride_r=1,
                                                                      stride_xi=2,
                                                                      stride_eta=2,
                                                                      use_r_padding=False))
        self.print_layer(self.layers, -1, 'activation')
        self.print_layer(self.layers, -1, 'pool')

            
        ### LAYER 4 ###
        self.layers.append({})
        self.layers[-1].update(self.create_cubed_sphere_conv_banded_disjoint_layer(len(self.layers)-1,
                                                                                   self.layers[-2]['pool'],
                                                                                   ksize_r=3,
                                                                                   ksize_xi=3,
                                                                                   ksize_eta=3,
                                                                                   channels_out=128,
                                                                                   stride_r=1,
                                                                                   stride_xi=1,
                                                                                   stride_eta=1,
                                                                                   use_r_padding=False))
        self.layers[-1]['activation'] = tf.nn.relu(self.layers[-1]['conv'])
        self.layers[-1].update(self.create_cubed_sphere_avgpool_layer(len(self.layers)-1,
                                                                      self.layers[-1]['activation'],
                                                                      ksize_r=1,
                                                                      ksize_xi=3,
                                                                      ksize_eta=3,
                                                                      stride_r=1,
                                                                      stride_xi=1,
                                                                      stride_eta=1,
                                                                      use_r_padding=False))
        self.print_layer(self.layers, -1, 'activation')
        self.print_layer(self.layers, -1, 'pool')

        ### LAYER 5 ###
        self.layers.append({})
        self.layers[-1].update(self.create_dense_layer(len(self.layers)-1,
                                                       self.layers[-2]['pool'],
                                                       output_size=2048))
        self.layers[-1]['activation'] = tf.nn.relu(self.layers[-1]['dense'])
        self.layers[-1]['dropout'] = tf.nn.dropout(self.layers[-1]['activation'], self.dropout_keep_prob)
        self.print_layer(self.layers, -1, 'W')
        self.print_layer(self.layers, -1, 'activation')

        ### LAYER 6 ###
        self.layers.append({})
        self.layers[-1].update(self.create_dense_layer(len(self.layers)-1,
                                                       self.layers[-2]['dropout'],
                                                       output_size=-1))
        self.layers[-1]['activation'] = tf.nn.relu(self.layers[-1]['dense'])
        self.layers[-1]['dropout'] = tf.nn.dropout(self.layers[-1]['activation'], self.dropout_keep_prob)
        self.print_layer(self.layers, -1, 'W')
        self.print_layer(self.layers, -1, 'activation')

        ### LAYER 7 ###
        self.layers.append({})
        self.layers[-1].update(self.create_dense_layer(len(self.layers)-1,
                                                       self.layers[-2]['dropout'],
                                                       output_size=output_size))
        self.layers[-1]['activation'] = tf.nn.softmax(self.layers[-1]['dense'])
        self.print_layer(self.layers, -1, 'W')
        self.print_layer(self.layers, -1, 'activation')
