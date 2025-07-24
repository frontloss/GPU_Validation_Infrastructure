namespace Intel.VPG.Display.Automation
{
    using System.Collections.Generic;

    class MP_Audio_Multi_Source_CS : MP_Audio_Single_Source_CS
    {
        public MP_Audio_Multi_Source_CS()
        {
            _audioInputSource = AudioInputSource.Multiple;
        }
    }
}
