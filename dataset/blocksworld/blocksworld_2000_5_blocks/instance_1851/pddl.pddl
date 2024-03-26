

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a d)
(ontable b)
(ontable c)
(on d c)
(ontable e)
(clear a)
(clear b)
(clear e)
)
(:goal
(and
(on a d)
(on b e)
(on c a))
)
)


