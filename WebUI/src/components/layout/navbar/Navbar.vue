<template>
  <nav class="navbar app-navbar navbar-toggleable-md">
    <div class="navbar-brand-container d-flex align-items-center justify-content-start">
      <a class="navbar-brand" href="#/dashboard">
        <i class="i-vuestic"></i>
      </a>
    </div>

    <div class="row navbar-container">

      <div class="menu-icon-container d-flex align-items-center justify-content-center justify-content-lg-start col">
        <a class="menu-icon i-menu-expanded" href="#" @click.prevent="toggleSidebar(false)" v-if="sidebarOpened"></a>
        <a class="menu-icon i-menu-collapsed" href="#" @click.prevent="toggleSidebar(true)" v-else></a>
      </div>

      <div class="offset-lg-8"></div>
      <div class="col nav-item dropdown navbar-dropdown d-flex align-items-center justify-content-center"></div>
      <!--<div class="col nav-item dropdown navbar-dropdown d-flex align-items-center justify-content-center"> </div>-->
      <!--<div class="col nav-item dropdown navbar-dropdown d-flex align-items-center justify-content-center" v-dropdown>-->
      <!--<a class="nav-link dropdown-toggle d-flex align-items-center justify-content" href="#" @click.prevent="closeMenu">-->
      <!--<span class="i-nav-messages notify"></span>-->
      <!--</a>-->
      <!--<div class="dropdown-menu">-->
      <!--<div class="dropdown-menu-content">-->
      <!--<a class="dropdown-item" href="#">-->
      <!--<span class="ellipsis">{{ $t('messages.new', {name: "Oleg M"})}}</span>-->
      <!--</a>-->
      <!--<a class="dropdown-item" href="#">-->
      <!--<span class="ellipsis">{{ $t('messages.new', {name: "Andrei H"})}}</span>-->
      <!--</a>-->
      <!--<div class="dropdown-item plain-link-item">-->
      <!--<a class="plain-link" href="#">{{'messages.all' | translate}}</a>-->
      <!--</div>-->
      <!--</div>-->
      <!--</div>-->
      <!--</div>-->
      <div class="col nav-item d-flex align-items-center justify-content-center">
        <a class="nav-link d-flex align-items-center justify-content" href="#" @click.prevent="$refs.msgModal.open()">
          <span class="i-nav-notification"></span> <!--notify-->
        </a>
      </div>
      <!--<language-selector :options="langs"></language-selector>-->
      <div class="col nav-item dropdown navbar-dropdown d-flex align-items-center justify-content-center" v-dropdown>
        <a class="nav-link dropdown-toggle d-flex align-items-center justify-content" href="#"
           @click.prevent="closeMenu">
          <span class="avatar-container">
            <img src="https://image.flaticon.com/icons/svg/701/701997.svg"/>
          </span>
        </a>
        <div class="dropdown-menu last">
          <div class="dropdown-menu-content">
            <div v-show="false" class="dropdown-item plain-link-item">
              <a class="plain-link" href="#">My Profile</a>
            </div>
            <div v-show="false" class="dropdown-item plain-link-item">
              <a class="plain-link" href="#" @click.prevent="showLanguageModal">{{'user.language' | translate}}</a>
            </div>
            <div class="dropdown-item plain-link-item" @click.prevent="logout">
              <a class="plain-link" href="#">Logout</a>
            </div>
          </div>
        </div>
      </div>
    </div>
    <vuestic-modal ref="msgModal" v-bind:large="true" :cancelClass="'none'" okText="close" :cancelText="''">
      <div slot="title">Messages</div>
      <div v-if="this.userData.messages.length < 1" class="text-center">
        <h4>You have no messages!</h4>
      </div>
      <div v-else class="row">
        <div class="col-xs-12 col-md-12">
          <div class="table-responsive">
            <table class="table table-striped first-td-padding">
              <thead>
              <tr>
                <td align="center">Time</td>
                <td align="center">Message</td>
              </tr>
              </thead>
              <tbody>
              <tr v-for="message in userData.messages">
                <td align="center" style="word-wrap: break-word">{{new Date(message.time * 1000).toLocaleString()}}</td>
                <td align="center" style="word-wrap: break-word">{{message.message}}</td>
              </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </vuestic-modal>
  </nav>
</template>

<script>
  import {mapGetters, mapActions, mapMutations} from 'vuex'
  import LanguageSelector from './LanguageSelector'
  import mixin from '../../../mixins.js'

  export default {
    name: 'navbar',

    mixins: [mixin],

    components: {
      LanguageSelector
    },

    data () {
      return {
        langs: [
          {
            code: 'gb',
            name: 'english'
          },
          {
            code: 'es',
            name: 'spanish'
          }
        ]
      }
    },
    mounted () {
      this.updateUserData()
      this.interval = setInterval(() => {
        this.updateUserData()
      }, 10000)
    },
    beforeDestroy () {
      clearInterval(this.interval)
    },

    computed: {
      ...mapGetters([
        'sidebarOpened',
        'toggleWithoutAnimation',
        'userData'
      ])
    },

    methods: {
      ...mapActions([
        'closeMenu',
        'toggleSidebar',
        'isToggleWithoutAnimation',
        'setAuth'
      ]),
      ...mapMutations([
        'setUserData'
      ])
    }
  }
</script>

<style lang="scss">
  @import "../../../sass/_variables.scss";
  @import "../../../../node_modules/bootstrap/scss/mixins/breakpoints";
  @import "../../../../node_modules/bootstrap/scss/functions";
  @import "../../../../node_modules/bootstrap/scss/variables";

  .navbar.app-navbar {
    .navbar-container {
      width: 100%;
      height: 100%;
      margin: 0;
    }

    height: $top-nav-height;
    padding-left: $nav-padding-left;
    padding-right: $nav-padding-right;
    background-color: $top-nav-bg;

    .avatar-container {
      display: inline-block;
      width: 50px;
      height: 50px;
      background-color: white;
      border-radius: 50%;
      border: 2px solid $lighter-gray;
      overflow: hidden;

      img {
        height: 100%;
        width: 100%;
        background-color: lighten($top-nav-bg, 20%);
      }
    }

    .menu-icon-container {
      padding: 0;
      font-size: $font-size-base;
    }

    .navbar-brand-container {
      position: absolute;
      z-index: 3;
      height: 100%;
      left: $navbar-brand-container-left;
      top: 0;
    }

    .nav-item {
      padding: 0;
      height: 100%;
    }

    .dropdown.navbar-dropdown {
      .dropdown-toggle {
        padding: 0;
        &:after {
          display: none;
        }
      }

      &.show {
        @include media-breakpoint-up(lg) {
          .dropdown-menu {
            left: auto;
            right: 0;
          }
        }
        &:after {
          position: absolute;
          bottom: -$dropdown-show-b;
          right: calc(50% - 10px);
          width: 0;
          height: 0;
          display: block;
          content: '';
          border-left: 10px solid transparent;
          border-right: 10px solid transparent;
          border-bottom: 10px solid $darkest-gray;
        }
      }

      .dropdown-menu {
        margin-top: $dropdown-show-b;
        padding-top: 0;
        width: 100%;
      }

      .dropdown-item {
        height: $navbar-dd-item-height;
        cursor: pointer;
        font-size: $font-size-base;

        &:hover, &:active, &:focus, &.active {
          outline: none;
        }

        &.plain-link-item {
          color: $brand-primary;

          &:hover, &:active, &:focus {
            background: $dropdown-background;
          }

          .plain-link {
            text-decoration: none;
          }
        }
      }
    }

    .notify {
      position: relative;

      &::after {
        content: '';
        position: absolute;
        right: -6px;
        top: -6px;
        background-color: $brand-primary;
        height: 12px;
        width: 12px;
        border-radius: 50%;
      }
    }

    .i-nav-notification.notify::after {
      right: -4px;
      top: 0;
    }

    @include media-breakpoint-down(md) {
      height: $top-mobile-nav-height;
      padding: $nav-mobile-pt $nav-mobile-padding-h $nav-mobile-pb $nav-mobile-padding-h;

      .navbar-brand-container {
        width: $nav-mobile-brand-width;
        top: $nav-mobile-brand-top;
        left: $nav-mobile-brand-left;
        height: auto;
        .navbar-brand {
          height: $font-size-smaller;
          padding: 0;
          font-size: $font-size-smaller;
        }
      }

      .dropdown.navbar-dropdown {
        &.show {
          display: flex;
          &:after {
            bottom: -$dropdown-mobile-show-b;
            z-index: 2;
          }
          .dropdown-menu {
            margin-top: $dropdown-mobile-show-b;
            left: auto;
            &.last {
              right: 0;
            }
          }
        }
      }
    }
  }
</style>
