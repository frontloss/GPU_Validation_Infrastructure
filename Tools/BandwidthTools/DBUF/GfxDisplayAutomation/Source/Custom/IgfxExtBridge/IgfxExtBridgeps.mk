
IgfxExtBridgeps.dll: dlldata.obj IgfxExtBridge_p.obj IgfxExtBridge_i.obj
	link /dll /out:IgfxExtBridgeps.dll /def:IgfxExtBridgeps.def /entry:DllMain dlldata.obj IgfxExtBridge_p.obj IgfxExtBridge_i.obj \
		kernel32.lib rpcndr.lib rpcns4.lib rpcrt4.lib oleaut32.lib uuid.lib \

.c.obj:
	cl /c /Ox /DWIN32 /D_WIN32_WINNT=0x0400 /DREGISTER_PROXY_DLL \
		$<

clean:
	@del IgfxExtBridgeps.dll
	@del IgfxExtBridgeps.lib
	@del IgfxExtBridgeps.exp
	@del dlldata.obj
	@del IgfxExtBridge_p.obj
	@del IgfxExtBridge_i.obj
