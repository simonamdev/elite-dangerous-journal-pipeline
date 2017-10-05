import gulp from 'gulp';
import sourceMaps from 'gulp-sourcemaps';
import browserify from 'browserify';
import babelify from 'babelify';
import source from 'vinyl-source-stream';
import buffer from 'vinyl-buffer';
import uglify from 'gulp-uglify';
import rename from 'gulp-rename';

let stripDirectory = (path) => {
    path.dirname = '';
}

gulp.task('build', () => {
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
