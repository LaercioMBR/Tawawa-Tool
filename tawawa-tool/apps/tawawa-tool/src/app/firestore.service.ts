import { Injectable } from '@angular/core';
import { AngularFirestore } from '@angular/fire/compat/firestore';
import { link_anime } from './models/link_anime';
import { link_manga  } from './models/link_manga';
import { link_mmo } from './models/link_mmo';


@Injectable({
  providedIn: 'root'
})
export class FirestoreService {

  constructor(private firestore : AngularFirestore) {

  }

  getLinkMMOs() {
    return this.firestore.collection<link_mmo>('links-mmo').valueChanges();
  }

  getLinkManga() {
    return this.firestore.collection<link_manga>('links-manga').valueChanges();
  }

  getLinkAnime() {
    return this.firestore.collection<link_anime>('links-anime').valueChanges();
  }

}
