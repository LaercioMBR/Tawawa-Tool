import { Component, OnInit } from '@angular/core';
import { FirestoreService } from '../firestore.service';

@Component({
  selector: 'tawawa-tool-manga-link-guide',
  templateUrl: './manga-link-guide.component.html',
  styleUrls: ['./manga-link-guide.component.scss'],
})
export class MangaLinkGuideComponent implements OnInit {
  link_manga: any[] = [];
  cols!: any[];

  constructor(firestoreService : FirestoreService,
  ) {

    firestoreService.getLinkManga().forEach( value =>  {

      this.link_manga = value;

    });

  }


  ngOnInit() {

    this.cols = [
      { field: 'name', header: 'Name' },
      { field: 'updateFrequency', header: 'Update Frequency' },
      { field: 'fullColored', header: 'Full Color' },
      { field: 'blackAndWhite', header: 'Black and White' },
      { field: 'blueMonochrome', header: 'Blue Monochrome' },
      { field: 'caughtUpLevel', header: 'Caught Up Level' },
      { field: 'convenience', header: 'Convenience' }

    ];
  }
}
