

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(ontable b)
(on c a)
(on d c)
(on e b)
(clear d)
(clear e)
)
(:goal
(and
(on a d)
(on b e)
(on c b)
(on e a))
)
)


