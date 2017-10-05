import gulp from 'gulp';
import replace from 'gulp-replace';
import sourceMaps from 'gulp-sourcemaps';
import browserify from 'browserify';
import babelify from 'babelify';
import source from 'vinyl-source-stream';
import buffer from 'vinyl-buffer';
import uglify from 'gulp-uglify';
import rename from 'gulp-rename';
import htmlmin from 'gulp-htmlmin';

let stripDirectory = (path) => {
    path.dirname = '';
}

gulp.task('build', ['build_js', 'build_html']);

gulp.task('build_js', () => {
    return browserify('./src/js/overlay.js')
        .transform(babelify)
        .bundle()
        .pipe(source('./src/js/overlay.js'))
        .pipe(buffer())
        .pipe(rename(stripDirectory))
        .pipe(gulp.dest('./dist'))
        .pipe(rename({suffix: '.min'}))
        .pipe(uglify())
        .pipe(gulp.dest('./dist'));
});

gulp.task('build_html', () => {
    return gulp.src('./src/html/overlay.html')
        .pipe(htmlmin({ collapseWhitespace: true }))
        .pipe(rename({suffix: '.min'}))
        .pipe(gulp.dest('./dist'));
});
