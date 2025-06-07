# /***************************************************************
# *   Project: Eye Controlled Wheelchair
# *   Developers: 
# *       - Gokul Subedi
# *       - Arjun Koirala
# *       - Sushmit Poudel
# *   Date: 2080-11-23
# *   Description: This code is part of the Eye Controlled Wheelchair project, developed as a minor project of the BEI 2077 batch. 
# *
# *   ©️ All rights reserved. This code is the intellectual property of the developers listed above. Unauthorized use, reproduction, 
#       or distribution of this code, in whole or in part, without prior written permission from the developers, is strictly prohibited and 
#       may be subject to legal action.
# *
# *   By accessing or using this code, you agree to abide by the following terms and conditions, which apply only if the developers 
#     permit the use of the code:
# *
# *   1. The code may be used, modified, and distributed for non-commercial purposes, provided proper attribution is given to the 
#         original developers.
# *   2. Any modifications made to the code must be clearly documented, and the original developers shall not be held liable for any 
#         issues arising from such modifications.
# *   3. This code is provided "as is," without warranty of any kind, express or implied, including but not limited to the warranties 
#         of merchantability, fitness for a particular purpose, and non-infringement.
# *   4. The developers or copyright holders shall not be liable for any claim, damages, or other liability, whether in an action of 
#         contract, tort, or otherwise, arising from, out of, or in connection with the code or the use or other dealings in the code.
# *
# *   Licensed under the Apache License, Version 2.0 (the "License");
# *   you may not use this file except in compliance with the License.
# *   You may obtain a copy of the License at
# *
# *       http://www.apache.org/licenses/LICENSE-2.0
# *
# *   Unless required by applicable law or agreed to in writing, software
# *   distributed under the License is distributed on an "AS IS" BASIS,
# *   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# *   See the License for the specific language governing permissions and
# *   limitations under the License.
# ***************************************************************/



import torch.nn as nn
from torchvision.models import resnet18
from torchvision.models.resnet import ResNet18_Weights

class EyeClassifier(nn.Module):
    def __init__(self, num_classes):
        super(EyeClassifier, self).__init__()
        # Use a pre-trained ResNet model
        self.resnet = resnet18(weights=ResNet18_Weights.IMAGENET1K_V1)
        # Replace the last fully connected layer
        num_features = self.resnet.fc.in_features
        self.resnet.fc = nn.Linear(num_features, num_classes)

    def forward(self, x):
        return self.resnet(x)