import { Component, OnInit } from '@angular/core';
import { FirestoreService } from '../firestore.service';

@Component({
  selector: 'tawawa-tool-anime-link-guide',
  templateUrl: './anime-link-guide.component.html',
  styleUrls: ['./anime-link-guide.component.scss'],
})
export class AnimeLinkGuideComponent implements OnInit {
  link_anime: any[] = [];
  cols!: any[];

  constructor(firestoreService : FirestoreService,
  ) {

    firestoreService.getLinkAnime().forEach( value =>  {

      this.link_anime = value;

    });

  }


  ngOnInit() {

    this.cols = [
      { field: 'name', header: 'Name' },
      { field: 'regionsAvailable', header: 'Regions Available' },
      { field: 'subtitlesLanguage', header: 'Subtitles Language' },
      { field: 'extras', header: 'Extras' },

    ];
  }
}
