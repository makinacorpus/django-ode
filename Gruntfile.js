module.exports = function(grunt) {

  // Project configuration.
    grunt.initConfig({
	pkg: grunt.file.readJSON('package.json'),
	bower: {
	    install: {
		options: {
		    copy: false
		}
	    }
	},
	copy: {
	    bootstrap: {
		expand: true,
		cwd: 'bower_components/bootstrap/dist/',
		src: ['js/**', 'css/**', 'fonts/**'],
		dest: 'static/'
	    },
	    datatables: {
		expand: true,
		cwd: 'bower_components/datatables/media/js/',
		src: ['jquery.dataTables.js'],
		dest: 'static/js/'
	    },
	    jquery: {
		expand: true,
		cwd: 'bower_components/jquery/',
		src: ['jquery.js'],
		dest: 'static/js/'
	    },
	    moment: {
		expand: true,
		cwd: 'bower_components/moment/',
		src: ['moment.js'],
		dest: 'static/js/'
	    },
	    bootstrap_daterangepicker_js: {
		expand: true,
		cwd: 'bower_components/bootstrap-daterangepicker/',
		src: ['daterangepicker.js'],
		dest: 'static/js/'
	    },
	    bootstrap_daterangepicker_css: {
		expand: true,
		cwd: 'bower_components/bootstrap-daterangepicker/',
		src: ['daterangepicker-bs3.css'],
		dest: 'static/css/'
	    }
	}
    });

  // Load the plugins
    grunt.loadNpmTasks('grunt-contrib-copy');
    grunt.loadNpmTasks('grunt-bower-task');

  // Default task(s).
    grunt.registerTask('default', ['bower:install', 'copy']);

};
