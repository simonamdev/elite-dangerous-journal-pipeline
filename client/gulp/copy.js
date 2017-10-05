import gulp from 'gulp';
import replace from 'gulp-replace';

gulp.task('copy', ['copy_html', 'copy_js']);

gulp.task('copy_html', () => {
    return gulp.src('./dist/overlay.min.html')
        .pipe(replace('../../dist/overlay.js', '{{ url_for(\'static\', filename=\'js/overlay.min.js\') }}'))
        .pipe(gulp.dest('../server/templates/'));
});

gulp.task('copy_js', () => {
    return gulp.src('./dist/overlay.min.js')
        .pipe(replace('http://127.0.0.1:5000/pipeline', 'http://edjp.purrcat.space/pipeline'))
        .pipe(gulp.dest('../server/static/js/'));
});

gulp.task('copy_dev', ['copy_html'], () => {
    return gulp.src('./dist/overlay.min.js')
        .pipe(gulp.dest('../server/static/js/'));
});
