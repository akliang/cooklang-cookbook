const api_url = process.env.COOKBOOK_API_URL;

exports.api_login_url = api_url + '/api_login/';
exports.api_register_url = api_url + '/api_register/';
exports.api_deleteaccount_url = api_url + '/api_delete/';
exports.api_changepassword_url = api_url + '/api_changepw/';
exports.api_viewrecipes_url = api_url + '/view/';
exports.api_viewrecipesbytoken_url = api_url + '/view_by_token/';
exports.api_addrecipe_url = api_url + '/add_desktop/';
exports.api_deleterecipe_url = api_url + '/delete/';
exports.api_bookmarkrecipe_url = api_url + '/bookmark/';
exports.api_viewbookmarkrecipes_url = api_url + '/view_bookmarks/';
//exports.api_exportrecipes_url = api_url + '/export/';

exports.cloudfront_url = process.env.CLOUDFRONT_URL;
exports.image_style = "fit-in";
exports.image_size = "600x1200";