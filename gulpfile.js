////////////////////////////////
// Setup
////////////////////////////////

// Gulp and package
const { src, dest, parallel, series, watch } = require('gulp')
const pjson = require('./package.json')

// Plugins
const autoprefixer = require('autoprefixer')
const browserSync = require('browser-sync').create()

const cssnano = require ('cssnano')
const imagemin = require('gulp-imagemin')
const pixrem = require('pixrem')
const plumber = require('gulp-plumber')
const postcss = require('gulp-postcss')
const reload = browserSync.reload
const rename = require('gulp-rename')
const sass = require('gulp-sass')
const spawn = require('child_process').spawn
const uglify = require('gulp-uglify-es').default

// Relative paths function
function pathsConfig(appName) {
  this.app = `./${pjson.name}`
  const vendorsRoot = 'node_modules'

  return {

    app: this.app,
    templates: `${this.app}/templates`,
    css: `${this.app}/static/css`,
    sass: `${this.app}/static/sass`,
    fonts: `${this.app}/static/fonts`,
    images: `${this.app}/static/images`,
    js: `${this.app}/static/js`,
    vendor_css: `${this.app}/static/vendor/css`,
    vendor_js: `${this.app}/static/vendor/js`,
  }
}

var paths = pathsConfig()

////////////////////////////////
// Tasks
////////////////////////////////


// Copy vendor JS into output folder
var copyVendorJs = function (done) {

  let vendor_js = [
      // bootstrap.bundle.min.js includes Popper, but not jQuery
      'node_modules/jquery/dist/jquery.min.js',
      'node_modules/jquery/dist/jquery.min.map',
      'node_modules/bootstrap/dist/js/bootstrap.bundle.min.js',
      'node_modules/bootstrap/dist/js/bootstrap.bundle.min.js.map',
      'node_modules/@sentry/browser/build/bundle.min.js',
      'node_modules/@sentry/browser/build/bundle.min.js.map',
      'node_modules/cookieconsent/build/cookieconsent.min.js',
  ];

  return src(vendor_js)
    .pipe(dest(paths.vendor_js));
};

// Copy vendor CSS into output folder
var copyVendorCss = function (done) {

  let vendor_css = [
      'node_modules/bootstrap/dist/css/bootstrap.min.css',
      'node_modules/bootstrap/dist/css/bootstrap.min.css.map',
      'node_modules/cookieconsent/build/**',
  ];

  return src(vendor_css)
    .pipe(dest(paths.vendor_css));
};

// Styles autoprefixing and minification
function styles() {
  var processCss = [
      autoprefixer(), // adds vendor prefixes
      pixrem(),       // add fallbacks for rem units
  ]

  var minifyCss = [
      cssnano({ preset: 'default' })   // minify result
  ]

  return src(`${paths.sass}/project.scss`)
    .pipe(sass({
      includePaths: [

        paths.sass
      ]
    }).on('error', sass.logError))
    .pipe(plumber()) // Checks for errors
    .pipe(postcss(processCss))
    .pipe(dest(paths.css))
    .pipe(rename({ suffix: '.min' }))
    .pipe(postcss(minifyCss)) // Minifies the result
    .pipe(dest(paths.css))
}

// Javascript minification
function scripts() {
  return src(`${paths.js}/project.js`)
    .pipe(plumber()) // Checks for errors
    .pipe(uglify()) // Minifies the js
    .pipe(rename({ suffix: '.min' }))
    .pipe(dest(paths.js))
}



// Image compression
function imgCompression() {
  return src(`${paths.images}/*`)
    .pipe(imagemin()) // Compresses PNG, JPEG, GIF and SVG images
    .pipe(dest(paths.images))
}


// Run django server
function runServer(cb) {
  var cmd = spawn('python', ['manage.py', 'runserver'], {stdio: 'inherit'})
  cmd.on('close', function(code) {
    console.log('runServer exited with code ' + code)
    cb(code)
  })
}

// Browser sync server for live reload
function initBrowserSync() {
    browserSync.init(
      [
        `${paths.css}/*.css`,
        `${paths.js}/*.js`,
        `${paths.templates}/*.html`
      ], {
        // https://www.browsersync.io/docs/options/#option-proxy
        proxy:  {
          target: 'django:8000',
          proxyReq: [
            function(proxyReq, req) {
              // Assign proxy "host" header same as current request at Browsersync server
              proxyReq.setHeader('Host', req.headers.host)
            }
          ]
        },
        // https://www.browsersync.io/docs/options/#option-open
        // Disable as it doesn't work from inside a container
        open: false
      }
    )
}

// Watch
function watchPaths() {
  watch(`${paths.sass}/*.scss`, styles)
  watch(`${paths.templates}/**/*.html`).on("change", reload)
  watch([`${paths.js}/*.js`, `!${paths.js}/*.min.js`], scripts).on("change", reload)
}

// Copy vendor CSS + JS
const copyAllVendor = parallel(
  copyVendorJs,
  copyVendorCss,
)

// Generate all assets
const generateAssets = parallel(
  copyAllVendor,

  styles,
  scripts,

  imgCompression
)

// Set up dev environment
const dev = parallel(
  initBrowserSync,
  watchPaths
)

exports.default = series(generateAssets, dev)
exports["generate-assets"] = generateAssets
exports["vendor"] = copyAllVendor
exports["dev"] = dev
