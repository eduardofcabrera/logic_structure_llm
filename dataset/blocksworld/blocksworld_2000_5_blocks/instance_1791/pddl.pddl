

(define (problem BW-rand-5)
(:domain blocksworld-4ops)
(:objects a b c d e )
(:init
(handempty)
(on a b)
(ontable b)
(ontable c)
(on d c)
(ontable e)
(clear a)
(clear d)
(clear e)
)
(:goal
(and
(on a d)
(on b c)
(on c e)
(on e a))
)
)


