/*
 * This file contains some old python tests that have been ported to Rust. The exersize the "edit
 * lifecycle" as well as creation of a "rich" release entity (linked to all other entity types) in
 * a single editgroup.
 */

extern crate fatcat;
extern crate fatcat_api_spec;
extern crate uuid;
extern crate iron;

use fatcat_api_spec::*;
use fatcat_api_spec::models::*;

mod helpers;
use helpers::{setup_client};

#[test]
fn test_api_rich_create() {

    let (client, mut server) = setup_client();
    let client = client.with_context(Context::new());

    let admin_id = "aaaaaaaaaaaabkvkaaaaaaaaae".to_string();

    let mut new_eg = Editgroup::new(admin_id);
    new_eg.description = Some("a unit test edit".to_string());
    let resp = client.create_editgroup(new_eg).wait().unwrap();
    let editgroup_id = match resp {
        CreateEditgroupResponse::SuccessfullyCreated(eg) => eg.id.unwrap(),
        _ => unreachable!()
    };

    let mut new_container = ContainerEntity::new("schmournal".to_string());
    new_container.publisher = Some("society of authors".to_string());
    new_container.issnl = Some("2222-3333".to_string());
    // extra=dict(a=2, i="zing"))),
    let resp = client.create_container(new_container, Some(editgroup_id.clone())).wait().unwrap();
    let container_id = match resp {
        CreateContainerResponse::CreatedEntity(ee) => ee.ident,
        _ => unreachable!()
    };

    let mut new_creator = CreatorEntity::new("anon y. mouse".to_string());
    new_creator.orcid = Some("0000-0002-1825-0097".to_string());
    // extra=dict(a=2, i="zing"))),
    let resp = client.create_creator(new_creator, Some(editgroup_id.clone())).wait().unwrap();
    let creator_id = match resp {
        CreateCreatorResponse::CreatedEntity(ee) => ee.ident,
        _ => unreachable!()
    };

    let new_work = WorkEntity::new();
    // extra=dict(a=2, i="zing"))),
    let resp = client.create_work(new_work, Some(editgroup_id.clone())).wait().unwrap();
    let work_id = match resp {
        CreateWorkResponse::CreatedEntity(ee) => ee.ident,
        _ => unreachable!()
    };

    // this stub work will be referenced
    let mut new_release = ReleaseEntity::new("derivative work".to_string());
    new_release.release_type = Some("journal-article".to_string());
    new_release.work_id = Some(work_id.clone());
    let mut contrib = ReleaseContrib::new();
    contrib.creator_id = Some(creator_id.clone());
    new_release.contribs = Some(vec![contrib]);
    new_release.doi = Some("10.1234/58".to_string());
    let mut rref = ReleaseRef::new();
    rref.title = Some("some other work".to_string());
    new_release.refs = Some(vec![rref]);
    // extra=dict(a=2, i="zing"))),
    let resp = client.create_release(new_release, Some(editgroup_id.clone())).wait().unwrap();
    let stub_release_id = match resp {
        CreateReleaseResponse::CreatedEntity(ee) => ee.ident,
        _ => unreachable!()
    };

    let mut new_release = ReleaseEntity::new("dummy work".to_string());
    new_release.release_type = Some("book".to_string());
    new_release.work_id = Some(work_id.clone());
    new_release.container_id = Some(container_id.clone());
    let mut contrib = ReleaseContrib::new();
    contrib.creator_id = Some(creator_id.clone());
    new_release.contribs = Some(vec![contrib]);
    new_release.doi = Some("10.1234/5678".to_string());
    let mut rref = ReleaseRef::new();
    rref.title = Some("some paper".to_string());
    rref.target_release_id = Some(stub_release_id.clone());
    new_release.refs = Some(vec![rref]);
    // extra=dict(f=7, b="loopy"))),
    let resp = client.create_release(new_release, Some(editgroup_id.clone())).wait().unwrap();
    let release_id = match resp {
        CreateReleaseResponse::CreatedEntity(ee) => ee.ident,
        _ => unreachable!()
    };

    let mut new_file = FileEntity::new();
    new_file.sha1 = Some("7d97e98f8af710c7e7fe703abc8f639e0ee507c4".to_string());
    new_file.size = Some(1234);
    new_file.releases = Some(vec![release_id.clone()]);
    // extra=dict(f=4, b="zing"))),
    let resp = client.create_file(new_file, Some(editgroup_id.clone())).wait().unwrap();
    let file_id = match resp {
        CreateFileResponse::CreatedEntity(ee) => ee.ident,
        _ => {
            println!("{:?}", resp);
            unreachable!()
        }
    };

    let resp = client.get_changelog(Some(1)).wait().unwrap();
    let last_change_id = match resp {
        GetChangelogResponse::Success(list) => list[0].index,
        _ => unreachable!()
    };

    match client.accept_editgroup(editgroup_id.clone()).wait().unwrap() {
        AcceptEditgroupResponse::MergedSuccessfully(_) => (),
        _ => unreachable!()
    };

    let resp = client.get_changelog(Some(1)).wait().unwrap();
    match resp {
        GetChangelogResponse::Success(list) => assert_eq!(list[0].index, last_change_id+1),
        _ => unreachable!()
    };

    // test that foreign key relations worked
    let re = match client.get_release(release_id.clone(), None).wait().unwrap() {
        GetReleaseResponse::FoundEntity(e) => e,
        _ => unreachable!()
    };
    assert_eq!(re.contribs.clone().unwrap()[0].clone().creator_id.unwrap(), creator_id);
    assert_eq!(re.work_id.unwrap(), work_id);
    assert_eq!(re.contribs.unwrap()[0].clone().creator_id.unwrap(), creator_id);
    assert_eq!(re.refs.unwrap()[0].clone().target_release_id.unwrap(), stub_release_id);

    let fe = match client.get_file(file_id, None).wait().unwrap() {
        GetFileResponse::FoundEntity(e) => e,
        _ => unreachable!()
    };
    assert_eq!(fe.releases.unwrap()[0], release_id.clone());

    // had a test for active_editgroup here, but that's soon-to-be-deprecated
 
    server.close().unwrap()
}