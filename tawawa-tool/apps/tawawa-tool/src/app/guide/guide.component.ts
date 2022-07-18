import { Component, OnInit } from '@angular/core';
import { AngularFirestore } from '@angular/fire/compat/firestore';
import { Observable } from 'rxjs';
import { link_mmo } from '../models/link_mmo';
import { TableModule } from 'primeng/table';

@Component({
  selector: 'tawawa-tool-guide',
  templateUrl: './guide.component.html',
  styleUrls: ['./guide.component.scss'],
})
export class GuideComponent implements OnInit {
  response!: Observable<link_mmo[]>

  link_mmos: any[] = [];
  cols!: any[];

  constructor(firestore: AngularFirestore,
  ) {

    firestore.collection<link_mmo>('links-mmo').valueChanges().forEach(  value =>  {

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
      { field: 'fullColored', header: 'Full Color' }



    ];
  }
}
