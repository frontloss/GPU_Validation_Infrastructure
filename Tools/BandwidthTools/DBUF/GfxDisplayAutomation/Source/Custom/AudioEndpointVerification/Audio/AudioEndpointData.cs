using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Text.RegularExpressions;
using System.Threading.Tasks;

namespace AudioEndpointVerification
{
    public class AudioEndpointData
    {
        public string activeAudioEndpoints { get; set; }
        public List<string> playBackDevices { get; set; }
        public string defaultPlayBackDevice { get; set; }
        private List<AudioDispInfo> displayData;
        public AudioEndpointData()
        {
            displayData = new List<AudioDispInfo>();
            displayData = CommonExtension.GetAudioDisplayInfo();
            playBackDevices = new List<string>();
            defaultPlayBackDevice = GetDefaultEndpoint();
            playBackDevices = GetPlaybackDevices();
            activeAudioEndpoints = playBackDevices.Count().ToString();
        }
        private string GetDefaultEndpoint()
        {
            MMDeviceEnumerator DevEnum = new MMDeviceEnumerator();
            MMDevice device = DevEnum.GetDefaultAudioEndpoint(EDataFlow.eRender, ERole.eMultimedia);
            return device.FriendlyName;
        }
        private List<string> GetPlaybackDevices()
        {
            List<string> curPlaybackDeveces = new List<string>();
            MMDeviceEnumerator DevEnum = new MMDeviceEnumerator();
            MMDeviceCollection enumAudioDisplayCollection = DevEnum.EnumerateAudioEndPoints(EDataFlow.eRender, EDeviceState.DEVICE_STATE_ACTIVE);
            for (int eachAudioEndPoint = 0; eachAudioEndPoint < enumAudioDisplayCollection.Count; eachAudioEndPoint++)
            {
                string modelName = string.Empty;
                Regex reg = new Regex("[^a-zA-Z-0-9]");
                MMDevice endPointDevice = enumAudioDisplayCollection[eachAudioEndPoint];
                modelName = reg.Replace(endPointDevice.FriendlyName, "");
                if (displayData.Any(CDN => CDN.CompleteDisplayName.Replace(" ", "").Contains(modelName.Trim())))
                    curPlaybackDeveces.Add(endPointDevice.FriendlyName);
            }
            return curPlaybackDeveces;
        }
    }
}
