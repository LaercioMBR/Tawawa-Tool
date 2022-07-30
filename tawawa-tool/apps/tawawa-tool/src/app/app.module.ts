import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppComponent } from './app.component';
import { NavbarComponent } from './navbar/navbar.component';
import { SharedModule } from 'primeng/api';
import { MenuModule } from 'primeng/menu';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { RouterModule } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { MenubarModule } from 'primeng/menubar';
import { GuideComponent } from './guide/guide.component';
import { ToolComponent } from './tool/tool.component';
import { MmoComponent } from './mmo/mmo.component';
import { AnimeComponent } from './anime/anime.component';
import { MangaComponent } from './manga/manga.component';
import { CardModule } from 'primeng/card';
import { DividerModule } from 'primeng/divider';
import { TableModule } from 'primeng/table';
import { AngularFireModule } from '@angular/fire/compat';
import { environment } from '../environments/environment';
import { AngularFirestoreModule } from '@angular/fire/compat/firestore';
import { MmoLinkGuideComponent } from './mmo-link-guide/mmo-link-guide.component';
import { MangaLinkGuideComponent } from './manga-link-guide/manga-link-guide.component';
import { AnimeLinkGuideComponent } from './anime-link-guide/anime-link-guide.component';
import { ButtonModule } from 'primeng/button';
import { FirestoreService } from './firestore.service';


@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    HomeComponent,
    GuideComponent,
    ToolComponent,
    MmoComponent,
    AnimeComponent,
    MangaComponent,
    MmoLinkGuideComponent,
    MangaLinkGuideComponent,
    AnimeLinkGuideComponent,
  ],
  imports: [
    BrowserModule,
    MenuModule,
    SharedModule,
    BrowserAnimationsModule,
    MenubarModule,
    CardModule,
    DividerModule,
    TableModule,
    ButtonModule,
    AngularFireModule.initializeApp(environment.firebaseConfig),
    AngularFirestoreModule,
    RouterModule.forRoot([
      { path: '', component: HomeComponent },
      { path: 'guide', component: GuideComponent },
      { path: 'tool', component: ToolComponent },
      { path: 'mmo', component: MmoComponent },
      { path: 'anime', component: AnimeComponent },
      { path: 'manga', component: MangaComponent },
    ]),
  ],
  providers: [FirestoreService],
  bootstrap: [AppComponent],
})
export class AppModule {}
