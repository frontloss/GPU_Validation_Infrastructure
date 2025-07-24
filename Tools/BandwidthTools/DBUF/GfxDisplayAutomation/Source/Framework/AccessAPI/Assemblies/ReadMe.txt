** Pre Requisites for Running the DFT Tests:

1) VC++ Redistributables 2013.
2) Diva Driver should have been installed in the system.
Driver Location: http://coreval-build.intel.com/overview/26.
3) In Execute.exe.config file, set UseDivaFramework="true".

** Pre Requisites for configure SDK type:
currently framework supports two type of SDK service. [ SDK v7.0 and SDK v8.0 ]
we can configure sdk type by modifying  Execute.exe.config file
   a. UseSDKType="New" framework will take new SDK [v8.0] path for any SDK service
   b. UseSDKType="Old" framework will take old SDK [v7.0] path for any SDK service
   c. UseSDKType="Default" framework will take default SDK path i.e if driver baseline is greter than 15.48
   it will take new SDK [v8.0] else old SDK [v7.0] path for any SDK service

