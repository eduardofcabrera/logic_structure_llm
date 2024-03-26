

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(ontable a)
(on b d)
(on c a)
(on d c)
(ontable e)
(clear b)
(clear e)
)
(:goal
(and
(on a d)
(on b e)
(on c b))
)
)


