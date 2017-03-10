
editPostButton = function(){
	$(".edit-blog").click(function(){

	subject=$(this).find(".subject").html();
	artical=$(this).find(".blog").html();
	blog_id=$(this).find(".blog-id").text();
	$("#edit-modal input[name=edit-subject]").val(subject);
	$("#edit-modal textarea[name=edit-artical]").val(artical);
	$("#edit-modal input[name=blog-id]").val(blog_id);
	
});
}

deletePostButton = function(){
	$(".delete-blog").click(function(){

	
	blog_id=$(this).find(".blog-id").text();
	$("#warning-modal input[name=blog-id]").val(blog_id);
	$("#error-modal .modal-message").html("You can only edit or delete your posts");
	
});
}
	

editCommentButton = function(){
	$(".edit-comment").click(function(){
		
		
	comment_id=$(this).find(".comment-id").text();
	comment=$(this).find(".comment").html();	
	$("#editcomment-modal input[name=comment-id]").val(comment_id);
	$("#editcomment-modal textarea[name=edit-comment]").val(comment);
	$("#error-modal .modal-message").html("You can only edit or delete your comments");

});
}
deleteCommentButton = function(){
	$(".delete-comment").click(function(){
	
	comment_id=$(this).find(".comment-id").text();
	$("#warning-modal input[name=comment-id]").val(comment_id);	
	$("#error-modal .modal-message").html("You can only edit or delete your comments");
	$("#warning-modal  .modal-warning-msg").html("Are you sure you want delete this comment ?");
	$("#warning-modal .confirm").attr("name","delete-comment");
	console.log(comment_id);
});
}	



$(document).ready(function(){
		editPostButton();
		deletePostButton();
		editCommentButton();
		deleteCommentButton();
		
})