﻿var letters = " ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.:,;#+~*?!(){}[]/\&%|<>".split('');
// var letters = " Ag_,*(".split(''); // ein Paar Test-Zeichen
var WIDTH = 25;
var HEIGHT = 34;
var FONT_SIZE = 34;
var BOTTOM_OFFSET = 8; // um die Baseline auszugleichen.... mit Schriftgröße anpassen!
var FONT_NAME = "Consolas";
var TEXT_COLOR = [255, 255, 255]; // r g b
var BG_COLOR = [0, 0, 0]; // r g b

// Save the current preferences
var startRulerUnits = app.preferences.rulerUnits;
var startTypeUnits = app.preferences.typeUnits;
var startDisplayDialogs = app.displayDialogs;

// Set Adobe Photoshop CS5 to use pixels and display no dialogs
app.preferences.rulerUnits = Units.PIXELS;
app.preferences.typeUnits = TypeUnits.PIXELS;
app.displayDialogs = DialogModes.NO;

// new document
var doc = app.documents.add(WIDTH * letters.length, HEIGHT);
app.activeDocument = doc; 
    
// text color
var textColor = new SolidColor();
textColor.rgb.red = TEXT_COLOR[0];
textColor.rgb.green = TEXT_COLOR[1];
textColor.rgb.blue = TEXT_COLOR[2];

// bg color
var bgColor = new SolidColor();
bgColor.rgb.red = BG_COLOR[0];
bgColor.rgb.green = BG_COLOR[1];
bgColor.rgb.blue = BG_COLOR[2];

var bg = doc.artLayers.add();
bg.name = 'background';
doc.activeLayer = bg;
doc.selection.selectAll();
doc.selection.fill(bgColor);
doc.selection.deselect();

// letters
for (var i = 0; i < letters.length; i++) {
    var layer = doc.artLayers.add();
    layer.kind = LayerKind.TEXT;
    
    var text = layer.textItem;
    text.contents = letters[i];
    text.size = FONT_SIZE;
    text.font = app.fonts.getByName(FONT_NAME).postScriptName;
    text.color = textColor;
    text.position = new Array(0, 0);
    
    var bounds = layer.bounds;
    var textWidth = bounds[2];
    var x = (WIDTH * i) + Math.floor((-(WIDTH - textWidth)/2));
    var y = HEIGHT - BOTTOM_OFFSET;
    text.position = new Array(x, y); //pixels from the left, pixels from the top
    
    // guides
    if (i != 0) {
        doc.guides.add(Direction.VERTICAL, (WIDTH * i));
    }
}

// Reset the application preferences
app.preferences.rulerUnits = startRulerUnits;
app.preferences.typeUnits = startTypeUnits;
app.displayDialogs = startDisplayDialogs;