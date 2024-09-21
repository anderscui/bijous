

# Context Encoder

Widely-used context encoder architectures:

* CNN(convolutional neural network)
* RNN(recurrent neural network)
* recursive neural network
* deep transformers

BiLSTM 有效地利用了一个 token 的过去和未来的信息，通过它 encode 的 token 信息携带了有效的上下文信息。它也因此成为上下文相关的文本表示的标准方法。

对于一个原始的文本输入（如句子），先将其划分为 token 序列，再获得每个 token 的 embedding 信息（与RNN一起训练，或者预训练），再将 embedding 信息输入 RNN。RNN 层之后，是 Tag Decoder。

对于 RNN 的输入，除了单纯的 word embedding，也可以合并入 char embedding，乃至于 POS、gazeteers 等特征数据。

简言之，Encoder 将输入表示为带有上下文信息的序列数据。

# Tag Decoder

Decoder 将 Encoder 的序列数据解码为 tag，主要有以下几种：

* MLP + softmax：将序列标注问题表示为多分类问题
* CRF：最常用的 decoder，SOTA
* RNN
* Pointer network


