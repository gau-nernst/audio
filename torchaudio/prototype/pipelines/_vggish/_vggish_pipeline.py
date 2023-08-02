from dataclasses import dataclass

import torch
import torchaudio

from ._vggish_impl import _SAMPLE_RATE, VGGish as _VGGish, VGGishInputProcessor as _VGGishInputProcessor


@dataclass
class VGGishBundle:
    """VGGish :cite:`45611` inference pipeline ported from
    `torchvggish <https://github.com/harritaylor/torchvggish>`__
    and `tensorflow-models <https://github.com/tensorflow/models/tree/master/research/audioset>`__.

    Example:
        >>> import torchaudio
        >>> from torchaudio.prototype.pipelines import VGGISH
        >>>
        >>> input_sr = VGGISH.sample_rate
        >>> input_proc = VGGISH.get_input_processor()
        >>> model = VGGISH.get_model()
        >>>
        >>> waveform, sr = torchaudio.load(
        >>>     "Chopin_Ballade_-1_In_G_Minor,_Op._23.mp3",
        >>> )
        >>> waveform = waveform.squeeze(0)
        >>> waveform = torchaudio.functional.resample(waveform, sr, input_sr)
        >>> mono_output = model(input_proc(waveform))
    """

    class VGGish(_VGGish):
        __doc__ = _VGGish.__doc__

    class VGGishInputProcessor(_VGGishInputProcessor):
        __doc__ = _VGGishInputProcessor.__doc__

    _weights_path: str

    @property
    def sample_rate(self) -> int:
        """Sample rate of input waveform expected by input processor and model.

        :type: int
        """
        return _SAMPLE_RATE

    def get_model(self) -> VGGish:
        """Constructs pre-trained VGGish model. Downloads and caches weights as necessary.

        Returns:
            VGGish: VGGish model with pre-trained weights loaded.
        """
        model = self.VGGish()
        path = torchaudio.utils.download_asset(self._weights_path)
        state_dict = torch.load(path)
        model.load_state_dict(state_dict)
        model.eval()
        return model

    def get_input_processor(self) -> VGGishInputProcessor:
        """Constructs input processor for VGGish.

        Returns:
            VGGishInputProcessor: input processor for VGGish.
        """
        return self.VGGishInputProcessor()


VGGISH = VGGishBundle("models/vggish.pt")
VGGISH.__doc__ = """Pre-trained VGGish :cite:`45611` inference pipeline ported from
    `torchvggish <https://github.com/harritaylor/torchvggish>`__
    and `tensorflow-models <https://github.com/tensorflow/models/tree/master/research/audioset>`__.

    Per the `documentation <https://github.com/tensorflow/models/tree/master/research/audioset/vggish>`__
    for the original model, the model is "trained on a large YouTube dataset (a preliminary version of
    what later became YouTube-8M)".
    """