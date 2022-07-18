import { Component, OnInit } from '@angular/core';
import { MenuItem } from 'primeng/api';

@Component({
  selector: 'tawawa-tool-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.scss'],
})
export class NavbarComponent implements OnInit {

  items!: MenuItem[];

  ngOnInit() {
      this.items = [
          {label: 'Home', icon: 'pi pi-fw pi-home', routerLink:'/'},
          {label: 'Guide', icon: 'pi pi-fw pi-book', routerLink:'guide'},
          {label: 'Tool', icon: 'pi pi-fw pi-pencil', routerLink:'tool'},
          {label: 'MMO', icon: 'pi pi-fw pi-file', routerLink:'mmo'},
          {label: 'Anime', icon: 'pi pi-fw pi-cog', routerLink:'anime'},
          {label: 'Manga', icon: 'pi pi-fw pi-cog', routerLink:'manga'},
      ];
  }

}



