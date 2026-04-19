// MODULE: db
// PURPOSE: SQLite schema and queries for entire app
// DEPENDS ON: nothing
// SAFE TO MODIFY: Yes, but keep table definitions consistent
// DO NOT TOUCH: ui/, auth/, loans/ (they will depend on this file)

import 'dart:io';

import 'package:drift/drift.dart';
import 'package:drift/native.dart';
import 'package:path/path.dart' as p;
import 'package:path_provider/path_provider.dart';

part 'database.g.dart';

@DataClassName('Book')
class Books extends Table {
  IntColumn get id => integer().autoIncrement()();
  TextColumn get title => text().withLength(min: 1, max: 200)();
  TextColumn get author => text().withLength(min: 1, max: 100)();
  TextColumn get category => text().withLength(max: 50)();
  IntColumn get quantity => integer()();
  IntColumn get availableQuantity => integer()();
  DateTimeColumn get createdAt => dateTime().withDefault(currentDateAndTime)();

  @override
  List<String> get customConstraints => [
        'CHECK ("quantity" >= 0)',
        'CHECK ("available_quantity" >= 0)',
      ];
}

@DataClassName('Member')
class Members extends Table {
  IntColumn get id => integer().autoIncrement()();
  TextColumn get name => text().withLength(min: 1, max: 100)();
  TextColumn get phone => text().withLength(max: 20)();
  TextColumn get email => text().withLength(max: 100).nullable()();
  DateTimeColumn get createdAt => dateTime().withDefault(currentDateAndTime)();
}

@DataClassName('Loan')
class Loans extends Table {
  IntColumn get id => integer().autoIncrement()();
  IntColumn get bookId => integer().references(Books, #id)();
  IntColumn get memberId => integer().references(Members, #id)();
  DateTimeColumn get borrowDate => dateTime().withDefault(currentDateAndTime)();
  DateTimeColumn get dueDate => dateTime()();
  DateTimeColumn get returnDate => dateTime().nullable()();
  TextColumn get status =>
      text().withLength(max: 20).withDefault(const Constant('borrowed'))();
}

@DataClassName('Admin')
class Admins extends Table {
  IntColumn get id => integer().autoIncrement()();
  TextColumn get username => text().withLength(min: 3, max: 50)();
  TextColumn get passwordHash => text()();
  DateTimeColumn get createdAt => dateTime().withDefault(currentDateAndTime)();
}

@DriftDatabase(tables: [Books, Members, Loans, Admins])
class AppDatabase extends _$AppDatabase {
  AppDatabase() : super(_openConnection());

  @override
  int get schemaVersion => 1;

  @override
  MigrationStrategy get migration => MigrationStrategy(
        onCreate: (Migrator m) async {
          await m.createAll();
          await into(admins).insert(
            AdminsCompanion.insert(
              username: 'admin',
              passwordHash: '1234',
            ),
          );
        },
      );
}

LazyDatabase _openConnection() {
  return LazyDatabase(() async {
    final dbFolder = await getApplicationDocumentsDirectory();
    final file = File(p.join(dbFolder.path, 'library.db'));
    return NativeDatabase.createInBackground(file);
  });
}
