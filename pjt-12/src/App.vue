<template>
  <div>
    <nav class="navbar navbar-dark bg-dark">
      <div class="container-fluid">
        <div class="d-flex align-items-center gap-3">
          <span class="navbar-brand mb-0 h1">MyTube</span>
          <router-link class="nav-link text-light" to="/">Home</router-link>
          <router-link class="nav-link text-light" to="/search">Search</router-link>
          <router-link class="nav-link text-light" to="/saved">Later</router-link>
          <router-link class="nav-link text-light" to="/channels">Channel</router-link>
          <router-link class="nav-link text-light" to="/chat">Chat</router-link>
        </div>
      </div>
    </nav>
    <router-view />
  </div>
</template>

<style>
.nav-link{color:#ffffff!important}
.nav-link:hover{color:#dddddd!important}
</style>
