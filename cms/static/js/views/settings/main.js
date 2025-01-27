define(['js/views/validation', 'codemirror', 'underscore', 'jquery', 'jquery.ui', 'js/utils/date_utils',
    'js/models/uploads', 'js/views/uploads', 'js/views/license', 'js/models/license',
    'common/js/components/views/feedback_notification', 'jquery.timepicker', 'date', 'gettext',
    'js/views/learning_info', 'js/views/instructor_info', 'edx-ui-toolkit/js/utils/string-utils'],
    function (ValidatingView, CodeMirror, _, $, ui, DateUtils, FileUploadModel,
        FileUploadDialog, LicenseView, LicenseModel, NotificationView,
        timepicker, date, gettext, LearningInfoView, InstructorInfoView, StringUtils) {
        var DetailsView = ValidatingView.extend({
            // Model class is CMS.Models.Settings.CourseDetails
            events: {
                'input input': 'updateModel',
                'input textarea': 'updateModel',
                // Leaving change in as fallback for older browsers
                'change input': 'updateModel',
                'change textarea': 'updateModel',
                'change select': 'updateModel',
                'change #course-category': 'updateSubCategory',
                'change #course-course-sale-type': 'disableCoursePrice',
                'click .remove-course-introduction-video': 'removeVideo',
                'focus #course-overview': 'codeMirrorize',
                'focus #course-about-sidebar-html': 'codeMirrorize',
                'mouseover .timezone': 'updateTime',
                // would love to move to a general superclass, but event hashes don't inherit in backbone :-(
                'focus :input': 'inputFocus',
                'blur :input': 'inputUnfocus',
                'click .action-upload-image': 'uploadImage',
                'click .add-course-learning-info': 'addLearningFields',
                'click .add-course-instructor-info': 'addInstructorFields',
                'click #published-in-ecommerce-retry': 'retryPublishInEcommerce'
            },

            initialize: function (options) {
                options = options || {};
                // fill in fields
                this.$el.find('#course-language').val(this.model.get('language'));
                this.$el.find('#course-difficulty-level').val(this.model.get('difficulty_level'));
                this.$el.find('#course-region').val(this.model.get('region'));
                this.$el.find('#course-orgs').val(this.model.get('org'));
                this.$el.find('#course-category').val(this.model.get('new_category'));
                this.$el.find('#course-subcategory').val(this.model.get('subcategory'));
                this.$el.find('#course-platform-visibility').val(this.model.get('platform_visibility'));
                this.$el.find('#course-premium').val(this.model.get('premium'));
                this.$el.find('#course-indexed-in-discovery').val(this.model.get('indexed_in_discovery'));
                this.$el.find('#course-published-in-ecommerce').val(this.model.get('published_in_ecommerce'));
                this.$el.find('#course-course-sale-type').val(this.model.get('course_sale_type'));
                var course_price = parseFloat(this.model.get('course_price')).toFixed(2)
                this.$el.find('#course-course-price').val(course_price);

                this.$el.find('#course-organization').val(this.model.get('org'));
                this.$el.find('#course-number').val(this.model.get('course_id'));
                this.$el.find('#course-run').val(this.model.get('run'));
                this.$el.find('.set-date').datepicker({ dateFormat: 'm/d/yy' });
                this.$el.find('#allow-review').val(this.model.get('allow_review'));

                // Avoid showing broken image on mistyped/nonexistent image
                this.$el.find('img').error(function () {
                    $(this).hide();
                });
                this.$el.find('img').load(function () {
                    $(this).show();
                });

                this.listenTo(this.model, 'invalid', this.handleValidationError);
                this.listenTo(this.model, 'change', this.showNotificationBar);
                this.selectorToField = _.invert(this.fieldToSelectorMap);
                // handle license separately, to avoid reimplementing view logic
                this.licenseModel = new LicenseModel({ asString: this.model.get('license') });
                this.licenseView = new LicenseView({
                    model: this.licenseModel,
                    el: this.$('#course-license-selector').get(),
                    showPreview: true
                });
                this.listenTo(this.licenseModel, 'change', this.handleLicenseChange);

                if (options.showMinGradeWarning || false) {
                    new NotificationView.Warning({
                        title: gettext('Course Credit Requirements'),
                        message: gettext('The minimum grade for course credit is not set.'),
                        closeIcon: true
                    }).show();
                }

                this.learning_info_view = new LearningInfoView({
                    el: $('.course-settings-learning-fields'),
                    model: this.model
                });

                this.instructor_info_view = new InstructorInfoView({
                    el: $('.course-instructor-details-fields'),
                    model: this.model
                });
                this.initSubCategory();
                //Disable course sale type if already exist or not indexed in discovery
                if (this.model.get('indexed_in_discovery') && this.model.get('course_sale_type') === null) {
                    this.$el.find('#course-course-sale-type').prop("disabled", false)
                }
                else {
                    this.$el.find('#course-course-sale-type').prop("disabled", true)
                }
                //Disable course price
                this.$el.find('#course-course-price').prop("disabled", true)
            },

            render: function () {
                // Clear any image preview timeouts set in this.updateImagePreview
                clearTimeout(this.imageTimer);

                DateUtils.setupDatePicker('start_date', this);
                DateUtils.setupDatePicker('end_date', this);
                DateUtils.setupDatePicker('certificate_available_date', this);
                DateUtils.setupDatePicker('enrollment_start', this);
                DateUtils.setupDatePicker('enrollment_end', this);
                DateUtils.setupDatePicker('upgrade_deadline', this);

                this.$el.find('#' + this.fieldToSelectorMap.overview).val(this.model.get('overview'));
                this.codeMirrorize(null, $('#course-overview')[0]);

                if (this.model.get('title') !== '') {
                    this.$el.find('#' + this.fieldToSelectorMap.title).val(this.model.get('title'));
                } else {
                    var displayName = this.$el.find('#' + this.fieldToSelectorMap.title).attr('data-display-name');
                    this.$el.find('#' + this.fieldToSelectorMap.title).val(displayName);
                }
                this.$el.find('#' + this.fieldToSelectorMap.subtitle).val(this.model.get('subtitle'));
                this.$el.find('#' + this.fieldToSelectorMap.duration).val(this.model.get('duration'));
                this.$el.find('#' + this.fieldToSelectorMap.description).val(this.model.get('description'));

                this.$el.find('#' + this.fieldToSelectorMap.short_description).val(this.model.get('short_description'));
                this.$el.find('#' + this.fieldToSelectorMap.about_sidebar_html).val(
                    this.model.get('about_sidebar_html')
                );
                this.codeMirrorize(null, $('#course-about-sidebar-html')[0]);

                this.$el.find('.current-course-introduction-video iframe').attr('src', this.model.videosourceSample());
                this.$el.find('#' + this.fieldToSelectorMap.intro_video).val(this.model.get('intro_video') || '');
                if (this.model.has('intro_video')) {
                    this.$el.find('.remove-course-introduction-video').show();
                } else this.$el.find('.remove-course-introduction-video').hide();

                this.$el.find('#' + this.fieldToSelectorMap.effort).val(this.model.get('effort'));

                var courseImageURL = this.model.get('course_image_asset_path');
                this.$el.find('#course-image-url').val(courseImageURL);
                this.$el.find('#course-image').attr('src', courseImageURL);

                var bannerImageURL = this.model.get('banner_image_asset_path');
                this.$el.find('#banner-image-url').val(bannerImageURL);
                this.$el.find('#banner-image').attr('src', bannerImageURL);

                var videoThumbnailImageURL = this.model.get('video_thumbnail_image_asset_path');
                this.$el.find('#video-thumbnail-image-url').val(videoThumbnailImageURL);
                this.$el.find('#video-thumbnail-image').attr('src', videoThumbnailImageURL);

                var pre_requisite_courses = this.model.get('pre_requisite_courses');
                pre_requisite_courses = pre_requisite_courses.length > 0 ? pre_requisite_courses : '';
                this.$el.find('#' + this.fieldToSelectorMap.pre_requisite_courses).val(pre_requisite_courses);

                if (this.model.get('entrance_exam_enabled') == 'true') {
                    this.$('#' + this.fieldToSelectorMap.entrance_exam_enabled).attr('checked', this.model.get('entrance_exam_enabled'));
                    this.$('.div-grade-requirements').show();
                } else {
                    this.$('#' + this.fieldToSelectorMap.entrance_exam_enabled).removeAttr('checked');
                    this.$('.div-grade-requirements').hide();
                }
                this.$('#' + this.fieldToSelectorMap.entrance_exam_minimum_score_pct).val(this.model.get('entrance_exam_minimum_score_pct'));
                this.$el.find('#' + this.fieldToSelectorMap.allow_review).attr(
                    'checked', JSON.parse(this.model.get('allow_review'))
                );

                var selfPacedButton = this.$('#course-pace-self-paced'),
                    instructorPacedButton = this.$('#course-pace-instructor-paced'),
                    paceToggleTip = this.$('#course-pace-toggle-tip');
                (this.model.get('self_paced') ? selfPacedButton : instructorPacedButton).attr('checked', true);
                if (this.model.canTogglePace()) {
                    selfPacedButton.removeAttr('disabled');
                    instructorPacedButton.removeAttr('disabled');
                    paceToggleTip.text('');
                } else {
                    selfPacedButton.attr('disabled', true);
                    instructorPacedButton.attr('disabled', true);
                    paceToggleTip.text(gettext('Course pacing cannot be changed once a course has started.'));
                }
                if (this.model.get('premium') == true) {
                    this.$('#' + this.fieldToSelectorMap.premium).attr('checked', this.model.get('premium'));
                }


                if (this.model.get('indexed_in_discovery') == true) {
                    this.$('#' + this.fieldToSelectorMap.indexed_in_discovery).attr('checked', this.model.get('indexed_in_discovery'));
                }

                if (this.model.get('published_in_ecommerce') == null) {
                    this.$("#field-course-published-in-ecommerce").hide();
                }
                else if (this.model.get('published_in_ecommerce') == true) {
                    this.$("#field-course-published-in-ecommerce").show();
                    this.$("#field-link-of-ecommerce").show();
                    this.$("#published-in-ecommerce-retry").hide();
                    this.$("#retry-text").hide();
                    this.$('#' + this.fieldToSelectorMap.published_in_ecommerce).val("Yes");
                }
                else {
                    this.$("#field-course-published-in-ecommerce").show();
                    this.$('#' + this.fieldToSelectorMap.published_in_ecommerce).val("No");
                }


                this.licenseView.render();
                this.learning_info_view.render();
                this.instructor_info_view.render();

                return this;
            },
            fieldToSelectorMap: {
                language: 'course-language',
                difficulty_level: 'course-difficulty-level',
                region: 'course-region',
                course_org: 'course-orgs',
                new_category: 'course-category',
                subcategory: 'course-subcategory',
                platform_visibility: 'course-platform-visibility',
                premium: 'course-premium',
                indexed_in_discovery: 'course-indexed-in-discovery',
                published_in_ecommerce: 'course-published-in-ecommerce',
                course_sale_type: 'course-course-sale-type',
                course_price: 'course-course-price',
                start_date: 'course-start',
                end_date: 'course-end',
                enrollment_start: 'enrollment-start',
                enrollment_end: 'enrollment-end',
                upgrade_deadline: 'upgrade-deadline',
                certificate_available_date: 'certificate-available',
                overview: 'course-overview',
                title: 'course-title',
                subtitle: 'course-subtitle',
                duration: 'course-duration',
                description: 'course-description',
                about_sidebar_html: 'course-about-sidebar-html',
                short_description: 'course-short-description',
                intro_video: 'course-introduction-video',
                effort: 'course-effort',
                course_image_asset_path: 'course-image-url',
                banner_image_asset_path: 'banner-image-url',
                video_thumbnail_image_asset_path: 'video-thumbnail-image-url',
                pre_requisite_courses: 'pre-requisite-course',
                entrance_exam_enabled: 'entrance-exam-enabled',
                entrance_exam_minimum_score_pct: 'entrance-exam-minimum-score-pct',
                course_settings_learning_fields: 'course-settings-learning-fields',
                add_course_learning_info: 'add-course-learning-info',
                add_course_instructor_info: 'add-course-instructor-info',
                course_learning_info: 'course-learning-info',
                allow_review: 'allow-review',
            },

            addLearningFields: function () {
                /*
                * Add new course learning fields.
                * */
                var existingInfo = _.clone(this.model.get('learning_info'));
                existingInfo.push('');
                this.model.set('learning_info', existingInfo);
            },


            addInstructorFields: function () {
                /*
                * Add new course instructor fields.
                * */
                var instructors = this.model.get('instructor_info').instructors.slice(0);
                instructors.push({
                    name: '',
                    title: '',
                    organization: '',
                    image: '',
                    bio: ''
                });
                this.model.set('instructor_info', { instructors: instructors });
            },


               retryPublishInEcommerce: function () {
                $("#published-in-ecommerce-retry i.fa.fa-refresh").addClass("fa-spin");
                var self = this;
                var course_id = $('#course-id').val();
                var course_price = $("#course-course-price").val();
                var course_name = $('#course-name').val();
                var course_type = $('#course-course-sale-type').val();
                if(course_type == 'paid'){
                    course_type = 'professional';
                }else{
                    course_type = 'audit';
                }
                var host = window.location.protocol + "//" + window.location.host;
                $.ajax({
                    type: "POST",
                    url: host + "/api/courses/v2/modification/" + course_id + "/",
                    data: JSON.stringify({
                        "course_type": course_type,
                        "course_price": course_price,
                        "display_name": course_name
                    }),
                    success: function (response) {
                        $("#published-in-ecommerce-retry i.fa.fa-refresh").removeClass("fa-spin")
                        if (response['status'] == 'Success') {
                            $("#field-course-published-in-ecommerce").show();
                            $("#field-link-of-ecommerce").show();
                            $("#published-in-ecommerce-retry").hide();
                            $("#retry-text").hide();
                            $('#' + self.fieldToSelectorMap.published_in_ecommerce).val("Yes");
                        }
                        if (response['status'] == 'Failed') {
                            $("#field-course-published-in-ecommerce").show();
                            $('#' + self.fieldToSelectorMap.published_in_ecommerce).val("No");
                        }
                    },
                    error: function (response) {
                        $("#published-in-ecommerce-retry i.fa.fa-refresh").removeClass("fa-spin")
                        
                    }
                });

            },


            updateTime: function (e) {
                var now = new Date(),
                    hours = now.getUTCHours(),
                    minutes = now.getUTCMinutes(),
                    currentTimeText = StringUtils.interpolate(
                        gettext('{hours}:{minutes} (current UTC time)'),
                        {
                            hours: hours,
                            minutes: minutes
                        }
                    );

                $(e.currentTarget).attr('title', currentTimeText);
            },
            initSubCategory: function () {
                var $categorySelect = this.$el.find('#' + this.fieldToSelectorMap.new_category)
                var $subCategorySelect = this.$el.find('#' + this.fieldToSelectorMap.subcategory)

                // find selected category
                var selectedCategoryValue = $categorySelect.val();
                var selectedSubCategoryValue = $subCategorySelect.val();

                // clean subcategory select from older options
                $subCategorySelect.empty();

                // if category found - populate subcategory select
                if (selectedCategoryValue) {
                    var subcat_list = ['-']
                    var subcat_list = subcat_list.concat(subcategories[selectedCategoryValue])
                    console.log(subcat_list)
                    subcat_list.forEach(function (subcategory) {
                        var subcat_id = Object.keys(subcategory)[0]
                        var subcat_name = Object.values(subcategory)[0]
                        // you can extract this line into separate function
                        var $option = $('<option/>').attr('value', subcat_id).html(subcat_name);

                        $subCategorySelect.append($option);
                    });
                }
                if (selectedSubCategoryValue) {
                    $('#course-subcategory option[value="' + selectedSubCategoryValue + '"]').attr('selected', 'selected');
                }
                else {
                    $('#course-subcategory option[value="0"]').attr('selected', 'selected');
                }
                //$subCategorySelect.value=selectedSubCategoryValue;
            },
            updateSubCategory: function () {
                //var $categorySelect =  $("#course-category");
                //var $subCategorySelect =  $("#course-subcategory");

                var $categorySelect = this.$el.find('#' + this.fieldToSelectorMap.new_category)
                var $subCategorySelect = this.$el.find('#' + this.fieldToSelectorMap.subcategory)

                // clean subcategory select from older options
                $subCategorySelect.empty();

                // find selected category
                var selectedCategoryValue = $categorySelect.val();

                // if category found - populate subcategory select
                if (selectedCategoryValue) {
                    var subcat_list = ['-']
                    var subcat_list = subcat_list.concat(subcategories[selectedCategoryValue])
                    console.log(subcat_list)
                    subcat_list.forEach(function (subcategory) {
                        var subcat_id = Object.keys(subcategory)[0]
                        var subcat_name = Object.values(subcategory)[0]
                        // you can extract this line into separate function
                        var $option = $('<option/>').attr('value', subcat_id).html(subcat_name);

                        $subCategorySelect.append($option);
                    });
                }
                $('#course-subcategory option[value="0"]').attr('selected', 'selected');
            },
            disableCoursePrice: function () {
                if (this.$el.find('#course-course-sale-type').val() === "free") {
                    this.$el.find('#course-course-price').prop("disabled", true)
                }
                else {
                    this.$el.find('#course-course-price').prop("disabled", true)
                }
            },
            updateModel: function (event) {
                var value;
                var index = event.currentTarget.getAttribute('data-index');
                switch (event.currentTarget.id) {
                    case 'course-learning-info-' + index:
                        value = $(event.currentTarget).val();
                        var learningInfo = this.model.get('learning_info');
                        learningInfo[index] = value;
                        this.showNotificationBar();
                        break;
                    case 'course-instructor-name-' + index:
                    case 'course-instructor-title-' + index:
                    case 'course-instructor-organization-' + index:
                    case 'course-instructor-bio-' + index:
                        value = $(event.currentTarget).val();
                        var field = event.currentTarget.getAttribute('data-field'),
                            instructors = this.model.get('instructor_info').instructors.slice(0);
                        instructors[index][field] = value;
                        this.model.set('instructor_info', { instructors: instructors });
                        this.showNotificationBar();
                        break;
                    case 'course-instructor-image-' + index:
                        instructors = this.model.get('instructor_info').instructors.slice(0);
                        instructors[index].image = $(event.currentTarget).val();
                        this.model.set('instructor_info', { instructors: instructors });
                        this.showNotificationBar();
                        this.updateImagePreview(event.currentTarget, '#course-instructor-image-preview-' + index);
                        break;
                    case 'course-image-url':
                        this.updateImageField(event, 'course_image_name', '#course-image');
                        break;
                    case 'banner-image-url':
                        this.updateImageField(event, 'banner_image_name', '#banner-image');
                        break;
                    case 'video-thumbnail-image-url':
                        this.updateImageField(event, 'video_thumbnail_image_name', '#video-thumbnail-image');
                        break;
                    case 'entrance-exam-enabled':
                        if ($(event.currentTarget).is(':checked')) {
                            this.$('.div-grade-requirements').show();
                        } else {
                            this.$('.div-grade-requirements').hide();
                        }
                        this.setField(event);
                        break;
                    case 'entrance-exam-minimum-score-pct':
                        // If the val is an empty string then update model with default value.
                        if ($(event.currentTarget).val() === '') {
                            this.model.set('entrance_exam_minimum_score_pct', this.model.defaults.entrance_exam_minimum_score_pct);
                        } else {
                            this.setField(event);
                        }
                        break;
                    case 'pre-requisite-course':
                        var value = $(event.currentTarget).val();
                        value = value == '' ? [] : [value];
                        this.model.set('pre_requisite_courses', value);
                        break;
                    // Don't make the user reload the page to check the Youtube ID.
                    // Wait for a second to load the video, avoiding egregious AJAX calls.
                    case 'course-introduction-video':
                        this.clearValidationErrors();
                        var previewsource = this.model.set_videosource($(event.currentTarget).val());
                        clearTimeout(this.videoTimer);
                        this.videoTimer = setTimeout(_.bind(function () {
                            this.$el.find('.current-course-introduction-video iframe').attr('src', previewsource);
                            if (this.model.has('intro_video')) {
                                this.$el.find('.remove-course-introduction-video').show();
                            } else {
                                this.$el.find('.remove-course-introduction-video').hide();
                            }
                        }, this), 1000);
                        break;
                    case 'course-pace-self-paced':
                    // Fallthrough to handle both radio buttons
                    case 'course-pace-instructor-paced':
                        this.model.set('self_paced', JSON.parse(event.currentTarget.value));
                        break;
                    case 'course-language':
                    case 'course-difficulty-level':
                    case 'course-region':
                    case 'course-orgs':
                    case 'course-category':
                    case 'course-subcategory':
                    case 'course-platform-visibility':
                    case 'course-course-price':
                    case 'course-premium':
                    case 'course-indexed-in-discovery':
                    case 'course-course-sale-type':
                    case 'course-effort':
                    case 'course-title':
                    case 'course-subtitle':
                    case 'course-duration':
                    case 'course-description':
                    case 'course-short-description':
                    case 'allow-review':
                        this.setField(event);
                        break;
                    default: // Everything else is handled by datepickers and CodeMirror.
                        break;
                }
            },
            updateImageField: function (event, image_field, selector) {
                this.setField(event);
                var url = $(event.currentTarget).val();
                var image_name = _.last(url.split('/'));
                // If image path is entered directly, we need to strip the asset prefix
                image_name = _.last(image_name.split('block@'));
                this.model.set(image_field, image_name);
                this.updateImagePreview(event.currentTarget, selector);
            },
            updateImagePreview: function (imagePathInputElement, previewSelector) {
                // Wait to set the image src until the user stops typing
                clearTimeout(this.imageTimer);
                this.imageTimer = setTimeout(function () {
                    $(previewSelector).attr('src', $(imagePathInputElement).val());
                }, 1000);
            },
            removeVideo: function (event) {
                event.preventDefault();
                if (this.model.has('intro_video')) {
                    this.model.set_videosource(null);
                    this.$el.find('.current-course-introduction-video iframe').attr('src', '');
                    this.$el.find('#' + this.fieldToSelectorMap.intro_video).val('');
                    this.$el.find('.remove-course-introduction-video').hide();
                }
            },
            codeMirrors: {},
            codeMirrorize: function (e, forcedTarget) {
                var thisTarget, cachethis, field, cmTextArea;
                if (forcedTarget) {
                    thisTarget = forcedTarget;
                    thisTarget.id = $(thisTarget).attr('id');
                } else if (e !== null) {
                    thisTarget = e.currentTarget;
                } else {
                    // e and forcedTarget can be null so don't deference it
                    // This is because in cases where we have a marketing site
                    // we don't display the codeMirrors for editing the marketing
                    // materials, except we do need to show the 'set course image'
                    // workflow. So in this case e = forcedTarget = null.
                    return;
                }

                if (!this.codeMirrors[thisTarget.id]) {
                    cachethis = this;
                    field = this.selectorToField[thisTarget.id];
                    this.codeMirrors[thisTarget.id] = CodeMirror.fromTextArea(thisTarget, {
                        mode: 'text/html', lineNumbers: true, lineWrapping: true
                    });
                    this.codeMirrors[thisTarget.id].on('change', function (mirror) {
                        mirror.save();
                        cachethis.clearValidationErrors();
                        var newVal = mirror.getValue();
                        if (cachethis.model.get(field) != newVal) {
                            cachethis.setAndValidate(field, newVal);
                        }
                    });
                    cmTextArea = this.codeMirrors[thisTarget.id].getInputField();
                    cmTextArea.setAttribute('id', thisTarget.id + '-cm-textarea');
                }
            },

            revertView: function () {
                // Make sure that the CodeMirror instance has the correct
                // data from its corresponding textarea
                var self = this;
                this.model.fetch({
                    success: function () {
                        self.render();
                        _.each(self.codeMirrors, function (mirror) {
                            var ele = mirror.getTextArea();
                            var field = self.selectorToField[ele.id];
                            mirror.setValue(self.model.get(field));
                        });
                        self.licenseModel.setFromString(self.model.get('license'), { silent: true });
                        self.licenseView.render();
                    },
                    reset: true,
                    silent: true
                });
            },
            setAndValidate: function (attr, value) {
                // If we call model.set() with {validate: true}, model fields
                // will not be set if validation fails. This puts the UI and
                // the model in an inconsistent state, and causes us to not
                // see the right validation errors the next time validate() is
                // called on the model. So we set *without* validating, then
                // call validate ourselves.
                this.model.set(attr, value);
                this.model.isValid();
            },

            showNotificationBar: function () {
                // We always call showNotificationBar with the same args, just
                // delegate to superclass
                ValidatingView.prototype.showNotificationBar.call(this,
                    this.save_message,
                    _.bind(this.saveView, this),
                    _.bind(this.revertView, this));
            },

            uploadImage: function (event) {
                event.preventDefault();
                var title = '',
                    selector = '',
                    image_key = '',
                    image_path_key = '';
                switch (event.currentTarget.id) {
                    case 'upload-course-image':
                        title = gettext('Upload your course image.');
                        selector = '#course-image';
                        image_key = 'course_image_name';
                        image_path_key = 'course_image_asset_path';
                        break;
                    case 'upload-banner-image':
                        title = gettext('Upload your banner image.');
                        selector = '#banner-image';
                        image_key = 'banner_image_name';
                        image_path_key = 'banner_image_asset_path';
                        break;
                    case 'upload-video-thumbnail-image':
                        title = gettext('Upload your video thumbnail image.');
                        selector = '#video-thumbnail-image';
                        image_key = 'video_thumbnail_image_name';
                        image_path_key = 'video_thumbnail_image_asset_path';
                        break;
                }

                var upload = new FileUploadModel({
                    title: title,
                    message: gettext('Files must be in JPEG or PNG format.'),
                    mimeTypes: ['image/jpeg', 'image/png']
                });
                var self = this;
                var modal = new FileUploadDialog({
                    model: upload,
                    onSuccess: function (response) {
                        var options = {};
                        options[image_key] = response.asset.display_name;
                        options[image_path_key] = response.asset.url;
                        self.model.set(options);
                        self.render();
                        $(selector).attr('src', self.model.get(image_path_key));
                    }
                });
                modal.show();
            },

            handleLicenseChange: function () {
                this.showNotificationBar();
                this.model.set('license', this.licenseModel.toString());
            }
        });

        return DetailsView;
    }); // end define()
