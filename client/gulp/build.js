import gulp from 'gulp';
import babel from 'gulp-babel';
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

gulp.task('build', ['build_server', 'build_client']);

gulp.task('build_server', () => {
    return gulp.src('./src/app.js')
        .pipe(sourceMaps.init())
        .pipe(babel())
        .pipe(sourceMaps.write('.'))
        .pipe(gulp.dest('./dist'));
});

gulp.task('build_client', () => {
    return browserify('./src/client.js')
        .transform(babelify)
        .bundle()
        .pipe(source('./src/client.js'))
        .pipe(buffer())
        .pipe(rename(stripDirectory))
        .pipe(gulp.dest('./dist'))
        .pipe(rename({suffix: '.min'}))
        .pipe(uglify())
        .pipe(gulp.dest('./dist'));
});
