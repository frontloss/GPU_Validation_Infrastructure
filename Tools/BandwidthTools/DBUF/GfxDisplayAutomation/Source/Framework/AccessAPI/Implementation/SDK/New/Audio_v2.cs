namespace Intel.VPG.Display.Automation
{
    using System;
    using igfxSDKLib;

    /*  Get set audio information through CUI SDK 8.0 */
    class Audio_v2 : FunctionalBase, ISDK
    {
        IDisplayAudio Audio;
        public object Set(object args)
        {
            GfxSDKClass GfxSDK = new GfxSDKClass();
            Audio = GfxSDK.Display.Audio;
            bool status = false;

            SetAudioParam param = args as SetAudioParam;
            if (param.setAudioInfo == SetAudioSource.SetAudioTopology)
            {
                status = EnableAudioFeature(param);
            }
            else if (param.audioWTVideo == AudioWTVideo.Enable)
            {
                Audio.AudioWithoutVideo = AUDIO_WITHOUT_VIDEO_STATUS.ENABLED;
                status = EnableAudioFeature(param);
            }
            else if (param.audioWTVideo == AudioWTVideo.Disable)
            {
                Audio.AudioWithoutVideo = AUDIO_WITHOUT_VIDEO_STATUS.DISABLED;
                status = EnableAudioFeature(param);
            }
            else
                Log.Fail("Audio input source parameter is incorrect");
            return status;
        }

        private bool EnableAudioFeature(SetAudioParam param)
        {            
            if (param.audioTopology == AudioInputSource.Single)
                Audio.AudioConfiguration = AUDIO_INPUT.INDEPENDENT_AUDIO;
            else
                Audio.AudioConfiguration = AUDIO_INPUT.CLONED_AUDIO;

            Audio.Set();
            return Audio.Error == (uint)AUDIO_ERROR_CODES.AUDIO_SUCCESS;
        }

        public object Get(object args)
        {
            Log.Fail("Method not implemented");
            throw new NotImplementedException();
        }

        public object GetAll(object args)
        {
            Log.Fail("Method not implemented");
            throw new NotImplementedException();
        }
    }
}
