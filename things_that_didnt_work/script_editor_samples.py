connectAttr -f layeredTexture2.outAlpha ramp2.vCoord;
// Result: Connected layeredTexture2.outAlpha to ramp2.uvCoord.vCoord.
disconnectAttr ramp1.outColor blinn1.color;
// Result: Disconnect ramp1.outColor from blinn1.color.
connectAttr -f ramp2.outColor blinn1.color;
// Result: Connected ramp2.outColor to blinn1.color.
setAttr "ramp2.colorEntryList[0].color" -type double3 1 0 0 ;
setAttr "ramp2.colorEntryList[1].color" -type double3 0 1 0 ;
removeMultiInstance -break true ramp2.colorEntryList[0];
// Warning: WARNING |  [ramp_rgb] ramp2: ramp only has a single element, result will be constant.
// Warning: WARNING |  [ramp_rgb] ramp2: ramp only has a single element, result will be constant.
// Warning: WARNING |  [ramp_rgb] ramp2: ramp only has a single element, result will be constant.
// Warning: WARNING |  [ramp_rgb] ramp2: ramp only has a single element, result will be constant.
// Undo: removeMultiInstance -break true ramp2.colorEntryList[0]
setAttr "ramp2.colorEntryList[0].position" 0.280597;
setAttr ramp2.colorEntryList[2].color -type double3 0.709544 0.290456 0;
setAttr ramp2.colorEntryList[2].position 0.489552;
setAttr "ramp2.colorEntryList[2].position" 0.0328358;
setAttr "ramp2.colorEntryList[0].position" 0.489552;
setAttr "ramp2.colorEntryList[1].color" -type double3 0 1 1 ;
setAttr "ramp2.colorEntryList[1].position" 0.886567;
setAttr "ramp2.colorEntryList[1].position" 1;
setAttr "ramp2.colorEntryList[2].position" 0;
setAttr "ramp2.colorEntryList[0].position" 0.513433;


https://www.youtube.com/watch?v=U1ZNHT8MJuo