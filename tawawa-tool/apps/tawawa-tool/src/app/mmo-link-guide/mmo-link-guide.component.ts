import { Component, OnInit } from '@angular/core';
import { FirestoreService } from '../firestore.service';

@Component({
  selector: 'tawawa-tool-mmo-link-guide',
  templateUrl: './mmo-link-guide.component.html',
  styleUrls: ['./mmo-link-guide.component.scss'],
})
export class MmoLinkGuideComponent implements OnInit {
  link_mmos: any[] = [];
  cols!: any[];

  constructor(firestoreService : FirestoreService,
  ) {

    firestoreService.getLinkMMOs().forEach(value =>  {

      this.link_mmos = value;

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
      { field: 'convenience', header: 'Convenience' },

    ];
  }

}
