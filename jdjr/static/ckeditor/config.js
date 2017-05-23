/**
 * @license Copyright (c) 2003-2016, CKSource - Frederico Knabben. All rights reserved.
 * For licensing, see LICENSE.md or http://ckeditor.com/license
 */

CKEDITOR.editorConfig = function( config ) {
	// Define changes to default configuration here. For example:
	// config.language = 'fr';
	// config.uiColor = '#AADC6E';
	config.font_names = '宋体/宋体;黑体/黑体;仿宋/仿宋;楷体/楷体;隶书/隶书;幼圆/幼圆;微软雅黑/微软雅黑;' + config.font_names;
	config.smiley_path = './static/ckeditor/plugins/smiley/images/';
	//CKEDITOR.addCss(".cke_editable{background-color: #1774c8}");
	
};
