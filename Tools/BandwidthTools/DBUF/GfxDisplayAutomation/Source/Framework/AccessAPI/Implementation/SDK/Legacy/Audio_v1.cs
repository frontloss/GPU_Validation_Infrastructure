namespace Intel.VPG.Display.Automation
{
    using System;
    using IgfxExtBridge_DotNet;

    /*  Get set audio information through CUI SDK 7.0 */
    class Audio_v1 : FunctionalBase, ISDK
    {
        private IGFX_ERROR_CODES igfxErrorCode = IGFX_ERROR_CODES.IGFX_SUCCESS;
        private string errorDesc = "";
        private const uint multSource = 2;
        private const uint singleSource = 1;

        public object Set(object args)
        {
            SetAudioParam param = args as SetAudioParam;
            IGFX_AUDIO_FEATURE_INFO audFeture = new IGFX_AUDIO_FEATURE_INFO();
            bool status = false;
            if (param.setAudioInfo == SetAudioSource.SetAudioTopology)
            {
                status = EnableAudioFeature(audFeture, param);
            }
            else if (param.audioWTVideo == AudioWTVideo.Enable)
            {
                audFeture.dwAudioWoutVideo = multSource;
                status = EnableAudioFeature(audFeture, param);
            }
            else if (param.audioWTVideo == AudioWTVideo.Disable)
            {
                audFeture.dwAudioWoutVideo = singleSource;
                status = EnableAudioFeature(audFeture, param);
            }
            else
                Log.Abort("Audio input source parameter is incorrect");
            return status;
        }

        private bool EnableAudioFeature(IGFX_AUDIO_FEATURE_INFO audFeture, SetAudioParam param)
        {
            audFeture.versionHeader.dwVersion = 1;
            if (param.audioTopology == AudioInputSource.Single)
                audFeture.dwAudioConfig = singleSource;
            else
                audFeture.dwAudioConfig = multSource;
            APIExtensions.DisplayUtil.SetAudioTopology(ref audFeture, out igfxErrorCode, out errorDesc);
            return igfxErrorCode == IGFX_ERROR_CODES.IGFX_SUCCESS;
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
