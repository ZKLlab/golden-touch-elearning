<template>
  <el-main>
    <div
      v-if="!loading"
      class="main-button-group"
    >
      <el-button
        v-if="!visible"
        size="small"
        type="primary"
        :loading="visibleLoading"
        @click="changeVisible(true)"
      >
        <font-awesome-icon icon="paper-plane" />
        发布课程
      </el-button>
      <el-button
        v-else
        size="small"
        type="danger"
        :loading="visibleLoading"
        @click="changeVisible(false)"
      >
        <font-awesome-icon icon="stop-circle" />
        停止发布课程
      </el-button>
      <el-button
        size="small"
        @click="showCourseNameEditDialog"
      >
        <font-awesome-icon icon="pencil-alt" />
        修改课程名称
      </el-button>
      <el-button
        size="small"
        @click="showCourseCategoryEditDialog"
      >
        <font-awesome-icon icon="tag" />
        类别：{{ category['name'] }}
      </el-button>
    </div>
    <el-page-header
      @back="back"
    >
      <div
        slot="content"
        class="header"
      >
        {{ name }}
        <template v-if="name !== abbr">
          ( {{ abbr }} )<br>
        </template>
        <span>{{ slug }}</span>
      </div>
    </el-page-header>
    <div
      v-loading="loading"
      style="margin-top: 20px"
    >
      <div>
        <el-button
          type="primary"
          size="small"
          @click="createLesson"
        >
          <font-awesome-icon icon="plus" />
          添加课时
        </el-button>
        <el-button
          size="small"
          plain
          :disabled="lessonsLoading"
          @click="pullData"
        >
          <font-awesome-icon
            icon="sync-alt"
            :spin="lessonsLoading"
          />
          刷新
        </el-button>
      </div>
      <el-table
        v-loading="lessonsLoading"
        :data="lessons"
        style="margin-top: 5px"
      >
        <template slot="empty">
          <template v-if="!lessonsLoading">
            没有符合条件的记录
          </template>
          <template v-else>
            &nbsp;
          </template>
        </template>
        <el-table-column
          prop="order"
          label="#"
          width="40"
        />
        <el-table-column
          prop="name"
          label="课时名称"
        />
        <el-table-column
          label="视频"
          width="120"
        >
          <template v-slot="scope">
            <el-button
              v-if="scope['row']['video_id'] !== null"
              size="small"
              type="primary"
              round
              @click="showLessonVideoPreviewDialog(scope['row']['video_id'])"
            >
              预览
              <font-awesome-icon icon="play-circle" />
            </el-button>
          </template>
        </el-table-column>
        <el-table-column
          width="180"
        >
          <template v-slot="scope">
            <el-button
              size="small"
              @click="lessonDetail(scope['row']['id'])"
            >
              课时详情
            </el-button>
            <el-button
              size="small"
              type="danger"
              @click="deleteLesson(scope['row']['id'])"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
    <el-dialog
      title="修改课程名称"
      :visible.sync="courseNameEditDialogVisible"
    >
      <CourseNameEdit
        v-if="!courseNameEditReset"
        :original-name="name"
        :original-abbr="abbr"
        :slug="slug"
        @success="courseNameEditDialogSuccess"
      />
    </el-dialog>
    <el-dialog
      title="修改课程类别"
      :visible.sync="courseCategoryEditDialogVisible"
    >
      <CourseCategoryEdit
        v-if="!courseCategoryEditReset"
        :original-category-name="category"
        :slug="slug"
        @success="courseCategoryEditDialogSuccess"
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
import axios from 'axios'
import CourseNameEdit from '../components/CourseNameEdit'
import CourseCategoryEdit from '../components/CourseCategoryEdit'
import LessonVideoPreview from '../components/LessonVideoPreview'

export default {
  name: 'CoursesDetail',
  components: {
    CourseNameEdit,
    CourseCategoryEdit,
    LessonVideoPreview,
  },
  data() {
    return {
      loading: false,
      slug: '',
      name: '',
      abbr: '',
      courseNameEditDialogVisible: false,
      courseNameEditReset: false,
      visible: null,
      visibleLoading: false,
      category: '',
      courseCategoryEditDialogVisible: false,
      courseCategoryEditReset: false,
      lessons: [],
      lessonsCancel: null,
      lessonsLoading: false,
      lessonVideoPreviewDialogVisible: false,
      videoId: null,
    }
  },
  beforeRouteUpdate(to, from, next) {
    this.slug = to.params['slug']
    this.update()
    next()
  },
  mounted() {
    this.slug = this.$route.params['slug']
    this.update()
  },
  methods: {
    update() {
      this.loading = true
      if (this.lessonsCancel !== null) {
        this.lessonsCancel()
        this.lessonsCancel = null
      }
      this.$axios.get(`/course/${this.slug}`).then((response) => {
        this.name = response.data['name']
        this.abbr = response.data['abbr']
        this.slug = response.data['slug']
        this.visible = response.data['visible']
        this.category = response.data['category']
        this.pullData()
      }).catch(() => {
        this.$message.error('无法连接到服务器，请检查网络后重试！')
      }).then(() => {
        this.loading = false
      })
    },
    pullData() {
      this.lessonsLoading = true
      if (this.lessonsCancel !== null) {
        this.lessonsCancel()
        this.lessonsCancel = null
      }
      this.$axios.get(`/course/${this.slug}/lessons`, {
        cancelToken: new axios.CancelToken((c) => {
          this.cancel = c
        }),
      }).then((response) => {
        this.lessons = response.data
      }).catch(() => {
        this.$message.error('无法连接到服务器，请检查网络后重试！')
      }).then(() => {
        this.lessonsCancel = null
        this.lessonsLoading = false
      })
    },
    back() {
      this.$router.push('/courses')
    },
    changeVisible(value) {
      this.$confirm(value ? '此操作将使该课程对所有人可见，是否继续？' : '此操作将使该课程对除志愿者以外的人不可见，是否继续？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.visibleLoading = true
        this.$axios.patch(`/course/${this.slug}`, {
          visible: value,
        }).then((response) => {
          this.visible = response.data['visible']
          this.$message.success(value ? '成功发布课程！' : '成功停止发布课程！')
        }).catch(() => {
          this.$message.error('无法连接到服务器，请检查网络后重试！')
        }).then(() => {
          this.visibleLoading = false
        })
      })
    },
    showCourseNameEditDialog() {
      this.courseNameEditReset = true
      this.$nextTick(() => {
        this.courseNameEditReset = false
        this.courseNameEditDialogVisible = true
      })
    },
    courseNameEditDialogSuccess(value) {
      this.courseNameEditDialogVisible = false
      this.name = value['name']
      this.abbr = value['abbr']
    },
    showCourseCategoryEditDialog() {
      this.courseCategoryEditReset = true
      this.$nextTick(() => {
        this.courseCategoryEditReset = false
        this.courseCategoryEditDialogVisible = true
      })
    },
    courseCategoryEditDialogSuccess(value) {
      this.courseCategoryEditDialogVisible = false
      this.category = value
    },
    createLesson() {
      const loading = this.$loading({
        lock: true,
        text: '正在创建课时',
      })
      this.$axios.post(`/course/${this.slug}/lesson`, {
        name: '未命名的课时',
      }).then((response) => {
        this.$message.success('成功创建课时')
        this.newLessonDetail(response.data['id'])
      }).catch(() => {
        this.$message.error('无法连接到服务器，请检查网络后重试！')
      }).then(() => {
        loading.close()
      })
    },
    lessonDetail(id) {
      this.$router.push(`/courses/${this.slug}/lessons/${id}`)
    },
    newLessonDetail(id) {
      this.$router.push({
        path: `/courses/${this.slug}/lessons/${id}`,
        query: {
          new: '1',
        },
      })
    },
    showLessonVideoPreviewDialog(videoId) {
      this.videoId = videoId
      this.lessonVideoPreviewDialogVisible = true
    },
    deleteLesson(id) {
      this.$confirm('此操作将永久删除该课时，是否继续？', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.loading = true
        this.$axios.delete(`/course/${this.slug}/lesson/${id}`).then(() => {
          this.$message.success('成功删除课时！')
          this.pullData()
        }).catch(() => {
          this.$message.error('无法连接到服务器，请检查网络后重试！')
        }).then(() => {
          this.loading = false
        })
      })
    }
  }
}
</script>

<style scoped>
  .main-button-group {
    float: right;
    margin-top: -4px;
  }

  .header {
    font-size: 15px;
    line-height: 1.4;
    position: relative;
    top: -6px;
  }

  .header span {
    font-size: 12px;
    position: absolute;
    white-space: nowrap;
  }

  .video-preview-dialog >>> .el-dialog__body {
    padding: 10px 0 0;
  }
</style>