<template>
  <el-main>
    <el-page-header
      class="header"
      @back="back"
    >
      <div
        v-if="name"
        slot="content"
        class="header"
      >
        课时{{ order }} - {{ name }}
        <el-button
          class="edit-name-button"
          size="mini"
          @click="showLessonNameEditDialog"
        >
          <font-awesome-icon icon="pencil-alt" />
          修改课时名称
        </el-button>
      </div>
    </el-page-header>
    <el-breadcrumb
      separator-class="el-icon-arrow-right"
      style="margin-top: 20px"
    >
      <el-breadcrumb-item
        :to="{path: '/courses'}"
      >
        课程管理
      </el-breadcrumb-item>
      <el-breadcrumb-item
        v-if="courseName !== ''"
        :to="{path: `/courses/${slug}`}"
      >
        {{ courseAbbr }}
      </el-breadcrumb-item>
      <el-breadcrumb-item
        v-if="courseName !== ''"
      >
        <el-dropdown
          size="small"
          @command="changeLesson"
        >
          <el-button
            type="text"
            style="padding: 0; border: 0"
          >
            {{ name }}
            <font-awesome-icon icon="caret-down" />
          </el-button>
          <el-dropdown-menu slot="dropdown">
            <el-dropdown-item
              v-for="lesson in lessons"
              :key="lesson.id"
              :command="lesson.id"
              :disabled="lesson.id === id"
            >
              课时{{ lesson.order }} - {{ lesson.name }}
            </el-dropdown-item>
          </el-dropdown-menu>
        </el-dropdown>
      </el-breadcrumb-item>
    </el-breadcrumb>
    <div
      v-loading="loading"
      style="margin-top: 30px"
    >
      <el-row :gutter="20">
        <el-col
          :xs="12"
          :sm="12"
          :md="12"
          :lg="8"
          :xl="6"
        >
          <el-card>
            <template slot="header">
              <template v-if="!loading">
                <template v-if="videoId === null">
                  <el-button
                    type="text"
                    class="card-action-button"
                    @click="showLessonVideoSelectDialog"
                  >
                    点击此处添加视频
                  </el-button>
                </template>
                <template v-else>
                  <el-button
                    type="text"
                    class="card-action-button"
                    style="color: red"
                    @click="removeVideo"
                  >
                    删除
                  </el-button>
                  <el-button
                    type="text"
                    class="card-action-button"
                    @click="showLessonVideoSelectDialog"
                  >
                    替换视频
                  </el-button>
                </template>
              </template>
              <strong>
                <font-awesome-icon icon="film" />
                课程视频
              </strong>
            </template>
            <div
              v-if="videoId !== null"
              class="video-cover"
              @click="lessonVideoPreviewDialogVisible = true"
            >
              <div class="video-cover-inner">
                <font-awesome-icon icon="play-circle" />
                预览视频
              </div>
              <el-image :src="videoCover" />
            </div>
            <NoVideoPlaceholder v-else />
          </el-card>
        </el-col>
      </el-row>
    </div>
    <el-dialog
      title="修改课时名称"
      :visible.sync="lessonNameEditDialogVisible"
    >
      <LessonNameEdit
        v-if="!lessonNameEditReset"
        :id="id"
        :slug="slug"
        :original-name="name"
        @success="lessonNameEditDialogSuccess"
      />
    </el-dialog>
    <el-dialog
      title="选择一个视频"
      :visible.sync="lessonVideoSelectDialogVisible"
    >
      <LessonVideoSelect
        v-if="!lessonVideoSelectEditReset"
        :id="id"
        :slug="slug"
        @success="lessonVideoSelectDialogSuccess"
      />
    </el-dialog>
    <el-dialog
      title="视频播放"
      class="video-preview-dialog"
      :visible.sync="lessonVideoPreviewDialogVisible"
    >
      <LessonVideoPreview
        v-if="lessonVideoPreviewDialogVisible"
        :video-id="videoId"
      />
    </el-dialog>
  </el-main>
</template>

<script>
import LessonNameEdit from '../components/LessonNameEdit';
import LessonVideoSelect from '../components/LessonVideoSelect';
import LessonVideoPreview from '../components/LessonVideoPreview';
import NoVideoPlaceholder from '../../../components/NoVideoPlaceholder';

export default {
  name: 'LessonDetail',
  components: {
    LessonVideoPreview,
    LessonVideoSelect,
    NoVideoPlaceholder,
    LessonNameEdit,
  },
  data() {
    return {
      loading: false,
      slug: '',
      id: '',
      name: '',
      order: null,
      courseName: '',
      courseAbbr: '',
      lessons: [],
      videoId: null,
      videoCover: '',
      lessonNameEditDialogVisible: false,
      lessonNameEditReset: false,
      lessonVideoSelectDialogVisible: false,
      lessonVideoSelectEditReset: false,
      lessonVideoPreviewDialogVisible: false,
    }
  },
  beforeRouteUpdate(to, from, next) {
    if (this.slug !== to.params['slug'] || this.id !== to.params['id']) {
      this.slug = to.params['slug']
      this.id = to.params['id']
      this.update()
    }
    next()
  },
  mounted() {
    if (this.slug !== this.$route.params['slug'] || this.id !== this.$route.params['id']) {
      this.slug = this.$route.params['slug']
      this.id = this.$route.params['id']
      this.update()
    }
  },
  methods: {
    update() {
      this.loading = true
      this.$axios.get(`/course/${this.slug}/lesson/${this.id}`).then((response) => {
        this.name = response.data['name']
        this.order = response.data['order']
        this.slug = response.data['course_slug']
        this.courseName = response.data['course_name']
        this.courseAbbr = response.data['course_abbr']
        this.lessons = response.data['lessons']
        this.videoId = response.data['video_id']
        this.videoCover = response.data['video_cover']
        if (this.$route.query['new'] === '1') {
          this.showLessonNameEditDialog()
          this.$router.replace(`/courses/${this.slug}/lessons/${this.id}`)
        }
      }).catch(() => {
        this.$message.error('无法连接到服务器，请检查网络后重试！')
      }).then(() => {
        this.loading = false
      })
    },
    back() {
      this.$router.push(`/courses/${this.slug}`)
    },
    changeLesson(command) {
      this.lessonDetail(command)
    },
    lessonDetail(id) {
      this.$router.push(`/courses/${this.slug}/lessons/${id}`)
    },
    showLessonNameEditDialog() {
      this.lessonNameEditReset = true
      this.$nextTick(() => {
        this.lessonNameEditReset = false
        this.lessonNameEditDialogVisible = true
      })
    },
    lessonNameEditDialogSuccess(value) {
      this.name = value['name']
      this.lessons = value['lessons']
      this.lessonNameEditDialogVisible = false
    },
    showLessonVideoSelectDialog() {
      this.lessonVideoSelectEditReset = true
      this.$nextTick(() => {
        this.lessonVideoSelectEditReset = false
        this.lessonVideoSelectDialogVisible = true
      })
    },
    lessonVideoSelectDialogSuccess(value) {
      this.videoId = value['video_id']
      this.videoCover = value['video_cover']
      this.lessonVideoSelectDialogVisible = false
    },
    removeVideo() {
      this.$confirm(`此操作将删除这个课时的视频，是否继续？`, '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        if (this.currentRow !== null && !this.loading) {
          this.loading = true
          this.$axios.patch(`/course/${this.slug}/lesson/${this.id}`, {
            video_id: null,
          }).then((response) => {
            this.videoId = response.data['video_id']
            this.videoCover = response.data['video_cover']
            this.$message.success('成功删除视频！')
          }).catch(() => {
            this.$message.error('无法连接到服务器，请检查网络后重试！')
          }).then(() => {
            this.loading = false
          })
        }
      })
    },
  },
}
</script>

<style scoped>
  .header {
    height: 24px;
  }

  .edit-name-button {
    position: relative;
    top: -2px;
    margin-left: 10px;
  }

  .card-action-button {
    padding: 2px 0;
    float: right;
    margin-left: 10px;
  }

  .video-cover {
    position: relative;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    user-select: none;
    cursor: pointer;
  }

  .video-cover >>> img {
    transition: transform 0.4s, opacity 0.4s;
    transform: scale(1.0);
    opacity: 1;
  }

  .video-cover:hover >>> img {
    transform: scale(1.1);
    opacity: 0.5;
  }

  .video-cover .video-cover-inner {
    transition: transform 0.4s, color 0.4s, text-shadow 0.4s;
    position: absolute;
    color: rgba(255, 255, 255, 0.9);
    text-shadow: 0 0 5px rgba(0, 0, 0, 0.5);
    z-index: 10;
    transform: scale(1.0);
    padding: 40px 0;
  }

  .video-cover:hover .video-cover-inner {
    color: rgba(0, 0, 0, 0.9);
    text-shadow: 0 0 10px rgba(255, 255, 255, 1);
    transform: scale(1.15);
  }

  .video-preview-dialog >>> .el-dialog__body {
    padding: 10px 0 0;
  }
</style>