-- first we need ffi module (variable must be declared local)
local ffi = require("ffi")

local XPLMlib = ""
if SYSTEM == "IBM" then
  -- Windows OS (no path and file extension needed)
  if SYSTEM_ARCHITECTURE == 64 then
    XPLMlib = "XPLM_64"  -- 64bit
  else
    XPLMlib = "XPLM"     -- 32bit
  end
elseif SYSTEM == "LIN" then
  -- Linux OS (we need the path "Resources/plugins/" here for some reason)
  if SYSTEM_ARCHITECTURE == 64 then
    XPLMlib = "Resources/plugins/XPLM_64.so"  -- 64bit
  else
    XPLMlib = "Resources/plugins/XPLM.so"     -- 32bit
  end
elseif SYSTEM == "APL" then
  -- Mac OS (we need the path "Resources/plugins/" here for some reason)
  XPLMlib = "Resources/plugins/XPLM.framework/XPLM" -- 64bit and 32 bit
else
  return -- this should not happen
end

-- load the lib and store in local variable
local XPLM = ffi.load(XPLMlib)

DataRef("crashed", "sim/flightmodel2/misc/has_crashed")
DataRef("ground", "sim/flightmodel2/gear/on_ground", writable, 0)

function reload_heading_file()

  if crashed >=1 or ground >=1 then
    logMsg("Reloadinggggggggggggg")
    load_situation(SYSTEM_DIRECTORY .. "/Output/situations/keepHeading.sit" )
  end
end


do_often("reload_heading_file()")









